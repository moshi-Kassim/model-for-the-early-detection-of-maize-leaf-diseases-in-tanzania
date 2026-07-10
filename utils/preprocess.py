import cv2
import numpy as np
from PIL import Image

IMAGE_SIZE = (128, 128)


def preprocess_image(image: Image.Image) -> np.ndarray:
    """Convert a PIL image to a model-ready batch (1, 128, 128, 3) in BGR order."""
    rgb = np.array(image.convert("RGB"))
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    resized = cv2.resize(bgr, IMAGE_SIZE)
    normalized = resized.astype("float32") / 255.0
    return np.expand_dims(normalized, axis=0)
