import hashlib
import io
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from tensorflow.keras.models import load_model

from database.db import get_all_diagnoses, get_diagnosis_stats, init_database, save_diagnosis, save_uploaded_image
from utils.labels import (
    CLASS_NAMES,
    CONFUSION_MATRIX_CNN,
    DISEASE_INFO,
    DISPLAY_NAMES,
    MODEL_METRICS,
    SCIENTIFIC_NAMES,
)
from utils.preprocess import preprocess_image
from utils.theme import CUSTOM_CSS, DISEASE_COLORS
from utils.validator import validate_maize_leaf

BASE_DIR = Path(__file__).resolve().parent
MODEL_CANDIDATES = [
    BASE_DIR / "model" / "corn_disease_cnn.h5",
    BASE_DIR / "data" / "corn_disease_cnn.h5",
]
SAMPLE_DIR = BASE_DIR / "assets" / "sample_images"

PAGES = {
    "Diagnose": "diagnose",
    "History": "history",
    "Performance": "performance",
    "About": "about",
}

st.set_page_config(
    page_title="Maize Leaf Disease Detector",
    page_icon="🌽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


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
    model = load_model(str(model_path))
    return model, str(model_path)


@st.cache_resource(show_spinner=False)
def autoload_database():
    return str(init_database())


def autoload_resources():
    """Preload model and database once when the app starts."""
    if "resources_ready" not in st.session_state:
        with st.spinner("Loading model and database..."):
            db_path = autoload_database()
            model, model_path = autoload_model()
            st.session_state.resources_ready = True
            st.session_state.db_path = db_path
            st.session_state.model_path = model_path
            st.session_state.model = model
    return st.session_state.model, st.session_state.model_path, st.session_state.db_path


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


def _image_fingerprint(image: Image.Image, uploaded_name: str | None = None) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    digest = hashlib.md5(buffer.getvalue()).hexdigest()[:12]
    name = uploaded_name or "image"
    return f"{name}:{digest}"


def _log_diagnosis_once(fingerprint: str, **kwargs) -> None:
    logged = st.session_state.setdefault("logged_diagnoses", set())
    if fingerprint in logged:
        return
    save_diagnosis(**kwargs)
    logged.add(fingerprint)


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


def render_probability_bars(probabilities: dict[str, float], highlight: str):
    items = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
    bars_html = ""
    for name, value in items:
        cls_key = next((k for k, v in DISPLAY_NAMES.items() if v == name), "Healthy")
        color = DISEASE_COLORS.get(cls_key, "#3d6b4f")
        label = f"<strong>{name}</strong>" if name == highlight else name
        bars_html += f"""
        <div class="prob-row">
            <div class="prob-row-header"><span>{label}</span><span>{value:.1f}%</span></div>
            <div class="prob-track">
                <div class="prob-fill" style="width:{value}%; background:{color};"></div>
            </div>
        </div>
        """
    st.markdown(bars_html, unsafe_allow_html=True)


def render_sidebar(model_path: str, db_path: str):
    stats = get_diagnosis_stats()

    st.sidebar.markdown(
        """
        <div class="sidebar-title">Maize Leaf Disease Detector</div>
        <div class="sidebar-sub">EASTC · Field diagnosis tool for maize foliar diseases in Tanzania</div>
        """,
        unsafe_allow_html=True,
    )

    page_label = st.sidebar.radio("Menu", list(PAGES.keys()), label_visibility="collapsed")
    page = PAGES[page_label]

    st.sidebar.markdown("---")
    st.sidebar.markdown("**System**")
    st.sidebar.caption("Model ready")
    st.sidebar.caption("Database connected")
    st.sidebar.code(Path(model_path).name, language=None)

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Records**")
    st.sidebar.metric("Total", stats["total"])
    col_a, col_b = st.sidebar.columns(2)
    col_a.metric("Accepted", stats["accepted"])
    col_b.metric("Rejected", stats["rejected"])

    st.sidebar.markdown("---")
    st.sidebar.caption("Custom CNN · 92.4% test accuracy")
    st.sidebar.caption("4 classes · 128×128 input")

    return page


def page_diagnose(model):
    render_page_header(
        "Diagnosis",
        "Upload a maize leaf photograph. Results appear automatically.",
    )

    col_upload, col_result = st.columns([1, 1], gap="large")

    with col_upload:
        st.markdown('<div class="panel"><div class="panel-title">Image input</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="notice">Only maize (corn) leaf images are accepted. '
            "Other plants, fruits, people, and objects are rejected before diagnosis.</div>",
            unsafe_allow_html=True,
        )

        uploaded = st.file_uploader(
            "Upload image",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
            help="Diagnosis starts automatically after upload.",
        )

        sample_files = sorted(SAMPLE_DIR.glob("*.*")) if SAMPLE_DIR.exists() else []
        if sample_files:
            st.caption("Sample images")
            sample_cols = st.columns(min(len(sample_files), 4))
            for i, sample_path in enumerate(sample_files[:4]):
                with sample_cols[i]:
                    thumb = Image.open(sample_path)
                    st.image(thumb, use_container_width=True)
                    label = sample_path.stem.replace("_", " ")
                    if st.button(label, key=f"sample_{i}", use_container_width=True):
                        st.session_state["active_sample"] = str(sample_path)

        image = None
        is_trusted_sample = False
        uploaded_name = None
        uploaded_bytes = None

        if uploaded is not None:
            uploaded_bytes = uploaded.getvalue()
            uploaded_name = uploaded.name
            image = Image.open(io.BytesIO(uploaded_bytes))
            st.session_state.pop("active_sample", None)
        elif st.session_state.get("active_sample"):
            sample_path = Path(st.session_state["active_sample"])
            if sample_path.exists():
                image = Image.open(sample_path)
                is_trusted_sample = True
                uploaded_name = sample_path.name

        if image is not None:
            st.image(image, caption="Selected image", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_result:
        st.markdown('<div class="panel"><div class="panel-title">Result</div>', unsafe_allow_html=True)

        if image is None:
            st.markdown(
                """
                <div class="empty-state">
                    <p><strong>No image selected</strong></p>
                    <p>Upload a photograph or choose one of the sample images.<br>
                    Diagnosis runs as soon as an image is provided.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            with st.spinner("Analyzing image..."):
                result = predict_disease(model, image, trusted_sample=is_trusted_sample)

            fingerprint = _image_fingerprint(image, uploaded_name)
            source = "sample" if is_trusted_sample else "upload"
            stored_path = None
            if uploaded_bytes and uploaded_name:
                stored_path = save_uploaded_image(uploaded_bytes, uploaded_name)

            if not result["valid"]:
                _log_diagnosis_once(
                    fingerprint,
                    status="rejected",
                    source=source,
                    image_filename=uploaded_name,
                    image_path=stored_path,
                    rejection_reason=result["message"],
                )
                st.markdown(
                    f'<div class="reject-panel"><h3>Image not accepted</h3><p>{result["message"]}</p></div>',
                    unsafe_allow_html=True,
                )
            else:
                _log_diagnosis_once(
                    fingerprint,
                    status="accepted",
                    source=source,
                    image_filename=uploaded_name,
                    image_path=stored_path,
                    predicted_class=result["class_key"],
                    display_name=result["display_name"],
                    confidence=result["confidence"],
                    probabilities=result["probabilities"],
                )

                color = DISEASE_COLORS.get(result["class_key"], "#3d6b4f")
                st.markdown(
                    f"""
                    <div class="result-panel" style="border-left-color: {color};">
                        <div class="result-label">Predicted condition</div>
                        <p class="result-disease">{result['display_name']}</p>
                        <p class="result-scientific">{result['scientific_name']}</p>
                        <p class="result-confidence">{result['confidence']:.1f}% <span>confidence</span></p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown("**Class probabilities**")
                render_probability_bars(result["probabilities"], result["display_name"])

                st.markdown("**Description**")
                st.info(result["info"]["description"])
                with st.expander("Symptoms and management"):
                    st.markdown(f"**Symptoms:** {result['info']['symptoms']}")
                    st.markdown(f"**Management:** {result['info']['management']}")

        st.markdown("</div>", unsafe_allow_html=True)


def page_history():
    render_page_header(
        "Diagnosis history",
        "Records are saved automatically to the local database.",
    )

    stats = get_diagnosis_stats()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total", stats["total"])
    c2.metric("Accepted", stats["accepted"])
    c3.metric("Rejected", stats["rejected"])
    rate = f"{stats['accepted'] / stats['total'] * 100:.0f}%" if stats["total"] else "—"
    c4.metric("Acceptance rate", rate)

    if stats["by_class"]:
        st.subheader("By disease class")
        class_df = pd.DataFrame(
            [{"Disease": name, "Count": count} for name, count in stats["by_class"].items()]
        )
        st.bar_chart(class_df.set_index("Disease"), height=240)

    records = get_all_diagnoses()
    if not records:
        st.info("No records yet. Upload a maize leaf image on the Diagnose page.")
        return

    table_rows = [
        {
            "ID": row["id"],
            "Date": row["created_at"],
            "Status": row["status"].capitalize(),
            "Disease": row["display_name"] or "—",
            "Confidence": f"{row['confidence']:.1f}%" if row["confidence"] else "—",
            "Source": row["source"],
            "Image": row["image_filename"] or "—",
        }
        for row in records
    ]
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)


def page_performance():
    render_page_header(
        "Model performance",
        "Evaluation metrics from the held-out test set.",
    )

    metrics = MODEL_METRICS["custom_cnn"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Test accuracy", f"{metrics['test_accuracy']:.1%}")
    c2.metric("Test loss", f"{metrics['test_loss']:.4f}")
    c3.metric("Architecture", "Custom CNN")
    c4.metric("Training images", "4,188")

    st.subheader("Per-class metrics")
    rows = [
        {
            "Class": DISPLAY_NAMES[cls],
            "Precision": m["precision"],
            "Recall": m["recall"],
            "F1-Score": m["f1"],
        }
        for cls, m in metrics["per_class"].items()
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Confusion matrix")
        cm_df = pd.DataFrame(
            CONFUSION_MATRIX_CNN,
            index=[DISPLAY_NAMES[c] for c in CLASS_NAMES],
            columns=[DISPLAY_NAMES[c] for c in CLASS_NAMES],
        )
        st.dataframe(cm_df, use_container_width=True)
    with col2:
        st.subheader("Model comparison")
        st.table(
            pd.DataFrame(
                [
                    {"Model": "Custom CNN", "Accuracy": "92.37%", "Loss": "0.3725"},
                    {"Model": "ResNet50", "Accuracy": "77.42%", "Loss": "0.5277"},
                ]
            )
        )


def page_about():
    render_page_header(
        "About",
        "Predictive deep learning model for early detection of maize leaf diseases in Tanzania.",
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Objective
        Allow farmers and extension officers to upload a maize leaf image
        and receive a disease diagnosis with confidence scores.

        ### Methodology
        - **Dataset:** PlantVillage maize subset (4,188 images)
        - **Model:** Custom CNN (92.37% test accuracy)
        - **Input:** 128×128 RGB images
        - **Split:** 80% train / 10% validation / 10% test
        - **Deployment:** Streamlit application with SQLite storage
        """)
    with col2:
        st.markdown("### Disease classes")
        for cls in CLASS_NAMES:
            st.markdown(
                f"- **{DISPLAY_NAMES[cls]}** — *{SCIENTIFIC_NAMES[cls]}*"
            )

    st.markdown("---")
    st.markdown("""
    ### Usage
    1. **Diagnose** — upload a maize leaf image; results appear automatically
    2. **History** — view saved diagnosis records
    3. **Performance** — review model evaluation metrics
    """)


def main():
    try:
        model, model_path, db_path = autoload_resources()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.stop()

    page = render_sidebar(model_path, db_path)

    if page == "diagnose":
        page_diagnose(model)
    elif page == "history":
        page_history()
    elif page == "performance":
        page_performance()
    else:
        page_about()


if __name__ == "__main__":
    main()
