"""Shared model loading and diagnosis logic for user and admin dashboards."""

import io
from pathlib import Path

import numpy as np
import streamlit as st
from PIL import Image
from tensorflow.keras.models import load_model

from utils.labels import CLASS_NAMES, DISPLAY_NAMES, DISEASE_INFO, SCIENTIFIC_NAMES
from utils.preprocess import preprocess_image
from utils.validator import validate_maize_leaf

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_CANDIDATES = [
    BASE_DIR / "model" / "corn_disease_cnn.h5",
    BASE_DIR / "data" / "corn_disease_cnn.h5",
]
SAMPLE_DIR = BASE_DIR / "assets" / "sample_images"


def resolve_model_path() -> Path:
    for path in MODEL_CANDIDATES:
        if path.exists():
            return path
    raise FileNotFoundError(
        "Model file not found. Place corn_disease_cnn.h5 in model/ or data/ folder."
    )


@st.cache_resource(show_spinner=False)
def autoload_model():
    model_path = resolve_model_path()
    # Model was saved with Keras 3 (TF 2.16+). TF 2.15 cannot load batch_shape InputLayer.
    model = load_model(str(model_path), compile=False, safe_mode=False)
    return model, str(model_path)


def autoload_resources():
    if "resources_ready" not in st.session_state:
        with st.spinner("Loading model..."):
            model, model_path = autoload_model()
            st.session_state.resources_ready = True
            st.session_state.model_path = model_path
            st.session_state.model = model
    return st.session_state.model, st.session_state.model_path


def predict_disease(model, image: Image.Image, *, trusted_sample: bool = False):
    batch = preprocess_image(image)
    probabilities = model.predict(batch, verbose=0)[0]

    is_valid, rejection_message = validate_maize_leaf(
        image, probabilities, trusted_sample=trusted_sample
    )
    if not is_valid:
        return {"valid": False, "message": rejection_message}

    predicted_idx = int(np.argmax(probabilities))
    class_key = CLASS_NAMES[predicted_idx]
    return {
        "valid": True,
        "class_key": class_key,
        "display_name": DISPLAY_NAMES[class_key],
        "scientific_name": SCIENTIFIC_NAMES[class_key],
        "confidence": float(probabilities[predicted_idx] * 100),
        "probabilities": {
            DISPLAY_NAMES[name]: float(probabilities[i] * 100)
            for i, name in enumerate(CLASS_NAMES)
        },
        "info": DISEASE_INFO[class_key],
    }


def resolve_diagnosis_image(uploaded, *, sample_key_prefix: str = "active_sample"):
    if uploaded is not None:
        st.session_state.pop(sample_key_prefix, None)
        return Image.open(io.BytesIO(uploaded.getvalue())), False

    sample_path_value = st.session_state.get(sample_key_prefix)
    if sample_path_value:
        sample_path = Path(sample_path_value)
        if sample_path.exists():
            return Image.open(sample_path), True

    return None, False


def render_page_header(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="page-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def streamlit_context_active() -> bool:
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        return get_script_run_ctx() is not None
    except Exception:
        return False


def ensure_streamlit(script_path: Path, *, default_port: int | None = None) -> None:
    """Launch Streamlit when the script is run with plain `python`."""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        if get_script_run_ctx() is not None:
            return
    except Exception:
        pass

    import subprocess
    import sys

    args = list(sys.argv[1:])
    if default_port is not None and not any(
        arg == "--server.port" or arg.startswith("--server.port=") for arg in args
    ):
        args = ["--server.port", str(default_port), *args]

    sys.exit(
        subprocess.call(
            [sys.executable, "-m", "streamlit", "run", str(script_path), *args]
        )
    )
