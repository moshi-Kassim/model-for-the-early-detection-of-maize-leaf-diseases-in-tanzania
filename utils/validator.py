import cv2
import numpy as np
from PIL import Image

from utils.labels import CLASS_NAMES

MAIZE_HEALTHY_HUE = (68, 92)
MAIZE_LESION_HUE = (8, 34)
OTHER_PLANT_HUE = (38, 58)
FIELD_MAIZE_HUE = (40, 56)


def _pixel_ratio(mask: np.ndarray) -> float:
    return float(np.count_nonzero(mask)) / mask.size


def _vegetation_mask(hsv: np.ndarray) -> np.ndarray:
    h, s, v = cv2.split(hsv)
    return (s > 20) & (v > 30)


def _hue_stats(h: np.ndarray, vegetation: np.ndarray) -> tuple[float, float]:
    if not np.any(vegetation):
        return 0.0, 0.0
    hues = h[vegetation]
    return float(np.median(hues)), float(np.percentile(hues, 90) - np.percentile(hues, 10))


def analyze_leaf_likeness(image: Image.Image) -> dict:
    """Extract color and shape features used to reject non-maize uploads."""
    rgb = np.array(image.convert("RGB"))
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)
    vegetation = _vegetation_mask(hsv)

    green = cv2.inRange(hsv, (28, 25, 35), (95, 255, 255))
    brown_tan = cv2.inRange(hsv, (5, 25, 35), (22, 255, 210))
    rust_orange = cv2.inRange(hsv, (8, 40, 45), (22, 255, 255))

    foliage = cv2.bitwise_or(green, brown_tan)
    foliage = cv2.bitwise_or(foliage, rust_orange)

    skin = cv2.inRange(hsv, (0, 20, 50), (25, 170, 255))
    blue = cv2.inRange(hsv, (95, 35, 35), (135, 255, 255))
    gray = cv2.inRange(hsv, (0, 0, 35), (180, 45, 210))

    mango_fruit = cv2.inRange(hsv, (10, 70, 70), (26, 255, 255))
    citrus_fruit = cv2.inRange(hsv, (18, 90, 90), (32, 255, 255))
    tropical_leaf = cv2.inRange(hsv, (35, 35, 35), (58, 255, 220))

    maize_healthy_hue = (
        (h >= MAIZE_HEALTHY_HUE[0]) & (h <= MAIZE_HEALTHY_HUE[1]) & vegetation
    )
    maize_lesion_hue = (
        (h >= MAIZE_LESION_HUE[0])
        & (h <= MAIZE_LESION_HUE[1])
        & (s > 35)
        & vegetation
    )
    other_plant_hue = (
        (h >= OTHER_PLANT_HUE[0])
        & (h <= OTHER_PLANT_HUE[1])
        & (s > 30)
        & vegetation
    )

    veg_count = max(int(np.count_nonzero(vegetation)), 1)
    maize_healthy_ratio = float(np.count_nonzero(maize_healthy_hue)) / veg_count
    maize_lesion_ratio = float(np.count_nonzero(maize_lesion_hue)) / veg_count
    other_plant_ratio = float(np.count_nonzero(other_plant_hue)) / veg_count
    hue_median, hue_span = _hue_stats(h, vegetation)
    tropical_leaf_ratio = _pixel_ratio(tropical_leaf)
    fruit_ratio = max(_pixel_ratio(mango_fruit), _pixel_ratio(citrus_fruit))
    foliage_ratio = _pixel_ratio(foliage)
    aspect_ratio = _green_region_aspect_ratio(green)
    saturation_median, texture_variance = _texture_stats(rgb, hsv, vegetation)

    return {
        "foliage_ratio": foliage_ratio,
        "green_ratio": _pixel_ratio(green),
        "rust_orange_ratio": _pixel_ratio(rust_orange),
        "skin_ratio": _pixel_ratio(skin),
        "object_ratio": _pixel_ratio(cv2.bitwise_or(blue, gray)),
        "fruit_ratio": fruit_ratio,
        "maize_healthy_hue_ratio": maize_healthy_ratio,
        "maize_lesion_ratio": maize_lesion_ratio,
        "maize_disease_hue_ratio": maize_lesion_ratio,
        "other_plant_green_ratio": other_plant_ratio,
        "tropical_leaf_ratio": tropical_leaf_ratio,
        "background_ratio": 1.0 - foliage_ratio,
        "aspect_ratio": aspect_ratio,
        "hue_median": hue_median,
        "hue_span": hue_span,
        "saturation_median": saturation_median,
        "texture_variance": texture_variance,
    }


def _texture_stats(
    rgb: np.ndarray, hsv: np.ndarray, vegetation: np.ndarray
) -> tuple[float, float]:
    _, s, _ = cv2.split(hsv)
    if not np.any(vegetation):
        return 0.0, 0.0

    saturation_median = float(np.median(s[vegetation]))
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    texture_variance = float(cv2.Laplacian(gray, cv2.CV_64F)[vegetation].var())
    return saturation_median, texture_variance


def _green_region_aspect_ratio(green_mask: np.ndarray) -> float:
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return 1.0
    contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(contour)
    if min(w, h) == 0:
        return 1.0
    return max(w, h) / min(w, h)


def _reject_other_plant_message() -> str:
    return (
        "This image is from another plant, not a **maize (corn) leaf**. "
        "Leaves from mango, banana, sugarcane, sorghum, and other crops are not supported. "
        "Please upload a clear maize leaf photo."
    )


def _is_tropical_broadleaf_not_maize(features: dict) -> bool:
    """Reject tropical broadleaves (mango, banana, etc.) that mimic field-green hue."""
    if features["maize_healthy_hue_ratio"] >= 0.03 or features["tropical_leaf_ratio"] < 0.88:
        return False

    # Mango-like: vivid color or heavy vein texture.
    if features["other_plant_green_ratio"] >= 0.95 and (
        features["saturation_median"] >= 185
        or features["texture_variance"] >= 950
    ):
        return True

    # Banana/plantain-like: waxy smooth broadleaf with uniform tropical green.
    return (
        features["other_plant_green_ratio"] >= 0.88
        and features["texture_variance"] < 100
        and features["hue_span"] <= 14
    )


def _symptoms_match_prediction(
    predicted_class: str,
    max_prob: float,
    features: dict,
) -> bool:
    """Require visible disease cues when the model predicts an infected class."""
    if predicted_class == "Healthy" or max_prob < 0.75:
        return True

    lesion_ratio = features["maize_lesion_ratio"]
    rust_ratio = features["rust_orange_ratio"]

    if predicted_class == "Common_Rust":
        return lesion_ratio >= 0.15 or rust_ratio >= 0.05
    if predicted_class == "Blight":
        return lesion_ratio >= 0.25
    if predicted_class == "Gray_Leaf_Spot":
        return lesion_ratio >= 0.05
    return True


def _is_similar_grass_not_maize(features: dict, max_prob: float) -> bool:
    """Reject sugarcane/sorghum-like leaves that share maize color but lack maize hue cues."""
    return (
        max_prob >= 0.85
        and features["other_plant_green_ratio"] >= 0.70
        and features["maize_healthy_hue_ratio"] < 0.05
        and features["maize_lesion_ratio"] < 0.06
    )


def _is_field_diseased_maize_photo(
    features: dict, predicted_class: str, max_prob: float
) -> bool:
    """Accept real field maize photos when the model is highly confident of disease."""
    if predicted_class not in ("Blight", "Gray_Leaf_Spot", "Common_Rust"):
        return False

    return (
        max_prob >= 0.88
        and features["foliage_ratio"] >= 0.65
        and features["green_ratio"] >= 0.45
        and features["maize_healthy_hue_ratio"] >= 0.15
        and features["skin_ratio"] < 0.25
        and features["fruit_ratio"] < 0.20
    )


def _is_field_maize_photo(features: dict, predicted_class: str, max_prob: float) -> bool:
    """Accept real-world close-up maize photos with uniform field-green color."""
    return (
        predicted_class == "Healthy"
        and max_prob >= 0.88
        and features["green_ratio"] >= 0.90
        and features["foliage_ratio"] >= 0.90
        and features["maize_lesion_ratio"] < 0.05
        and features["texture_variance"] >= 80
        and features["hue_span"] <= 14
        and FIELD_MAIZE_HUE[0] <= features["hue_median"] <= FIELD_MAIZE_HUE[1]
    )


def validate_maize_leaf(
    image: Image.Image,
    probabilities: np.ndarray,
    *,
    trusted_sample: bool = False,
) -> tuple[bool, str]:
    """Return (is_valid, message). Rejects non-maize images before showing results."""
    if trusted_sample:
        return True, ""

    features = analyze_leaf_likeness(image)
    predicted_idx = int(np.argmax(probabilities))
    predicted_class = CLASS_NAMES[predicted_idx]

    sorted_probs = np.sort(probabilities)[::-1]
    max_prob = float(sorted_probs[0])
    margin = float(sorted_probs[0] - sorted_probs[1])

    if _is_tropical_broadleaf_not_maize(features):
        return False, _reject_other_plant_message()

    if _is_field_maize_photo(features, predicted_class, max_prob):
        return True, ""

    if _is_field_diseased_maize_photo(features, predicted_class, max_prob):
        return True, ""

    foliage_ratio = features["foliage_ratio"]
    green_ratio = features["green_ratio"]
    skin_ratio = features["skin_ratio"]
    object_ratio = features["object_ratio"]
    fruit_ratio = features["fruit_ratio"]
    maize_healthy_hue_ratio = features["maize_healthy_hue_ratio"]
    maize_lesion_ratio = features["maize_lesion_ratio"]
    other_plant_ratio = features["other_plant_green_ratio"]
    tropical_leaf_ratio = features["tropical_leaf_ratio"]
    background_ratio = features["background_ratio"]
    aspect_ratio = features["aspect_ratio"]
    hue_span = features["hue_span"]
    hue_median = features["hue_median"]

    maize_signal = maize_healthy_hue_ratio + maize_lesion_ratio

    if _is_similar_grass_not_maize(features, max_prob):
        return False, _reject_other_plant_message()

    if not _symptoms_match_prediction(predicted_class, max_prob, features):
        return False, (
            "The model prediction does not match what is visible in the image. "
            "This may be a **non-maize leaf** (e.g. sugarcane or another crop). "
            "Please upload a clear maize leaf photo."
        )

    if (
        other_plant_ratio >= 0.55
        and maize_healthy_hue_ratio < 0.12
        and maize_lesion_ratio < 0.05
        and hue_span >= 15
    ):
        return False, _reject_other_plant_message()

    if (
        background_ratio >= 0.20
        and other_plant_ratio >= 0.45
        and maize_healthy_hue_ratio < 0.15
        and maize_lesion_ratio < 0.06
        and hue_span >= 15
    ):
        return False, _reject_other_plant_message()

    if (
        tropical_leaf_ratio >= 0.45
        and maize_healthy_hue_ratio < 0.12
        and maize_lesion_ratio < 0.05
        and aspect_ratio < 2.0
        and hue_span >= 15
    ):
        return False, _reject_other_plant_message()

    if skin_ratio >= 0.22 and foliage_ratio < 0.30:
        return False, (
            "This image appears to contain a person or portrait. "
            "Please upload a clear photo of a **maize (corn) leaf** only."
        )

    if fruit_ratio >= 0.40 and green_ratio < 0.10:
        return False, (
            "This image looks like a fruit (e.g. mango, orange, banana), not a maize leaf. "
            "Please upload a **maize (corn) leaf** photo only."
        )

    if fruit_ratio >= 0.35 and green_ratio < 0.15 and maize_lesion_ratio < 0.50:
        return False, (
            "This image looks like a fruit (e.g. mango, orange, banana), not a maize leaf. "
            "Please upload a **maize (corn) leaf** photo only."
        )

    if fruit_ratio >= 0.14 and green_ratio < 0.22 and maize_lesion_ratio < 0.15:
        return False, (
            "This image looks like a fruit (e.g. mango, orange, banana), not a maize leaf. "
            "Please upload a **maize (corn) leaf** photo only."
        )

    if fruit_ratio >= 0.22 and maize_signal < 0.30:
        return False, (
            "This image appears to show fruit or a non-maize plant. "
            "This tool only accepts **maize (corn) leaves**."
        )

    if object_ratio >= 0.42 and foliage_ratio < 0.14:
        return False, (
            "This image appears to show an object, vehicle, or scene — not a plant leaf. "
            "Please upload a **maize leaf** photo."
        )

    if foliage_ratio < 0.16:
        return False, (
            "This does not look like a maize leaf. "
            "Upload a close-up photo of a single **maize (corn) leaf** with visible leaf tissue."
        )

    if predicted_class == "Healthy":
        if maize_healthy_hue_ratio < 0.15 and (
            hue_median > 56 or hue_median < FIELD_MAIZE_HUE[0] or hue_span >= 15
        ):
            return False, _reject_other_plant_message()
        if maize_healthy_hue_ratio < 0.42 and hue_span >= 15:
            return False, _reject_other_plant_message()
        if (
            tropical_leaf_ratio >= 0.28
            and maize_healthy_hue_ratio < 0.55
            and aspect_ratio < 2.0
            and hue_span >= 15
        ):
            return False, _reject_other_plant_message()

    if (
        predicted_class == "Healthy"
        and max_prob >= 0.85
        and maize_healthy_hue_ratio < 0.50
        and maize_lesion_ratio < 0.12
        and hue_span >= 15
    ):
        return False, _reject_other_plant_message()

    if max_prob < 0.55 and foliage_ratio < 0.38:
        return False, (
            "The model is not confident this is a maize leaf image. "
            "Please upload a clearer close-up of a **maize leaf**."
        )

    if margin < 0.12 and foliage_ratio < 0.28 and max_prob < 0.80:
        return False, (
            "The image is ambiguous and may not be a maize leaf. "
            "Try a closer photo of one maize leaf against a plain background."
        )

    return True, ""
