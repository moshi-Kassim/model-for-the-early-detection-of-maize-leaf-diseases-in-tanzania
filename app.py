"""Admin dashboard — detailed diagnosis, model performance, and project info."""

from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image

from utils.dashboard_core import (
    autoload_resources,
    ensure_streamlit,
    predict_disease,
    render_page_header,
    resolve_diagnosis_image,
    streamlit_context_active,
)
from utils.labels import (
    CLASS_NAMES,
    CONFUSION_MATRIX_CNN,
    DISPLAY_NAMES,
    MODEL_METRICS,
    SCIENTIFIC_NAMES,
)
from utils.community_ui import COMMUNITY_CSS, render_community_page
from utils.shared_diagnosis import load_user_diagnosis_batch
from utils.theme import CUSTOM_CSS, DISEASE_COLORS

PAGES = {
    "User Diagnosis": "user_diagnosis",
    "Community Help": "community",
    "Diagnose": "diagnose",
    "Performance": "performance",
    "About": "about",
}

st.set_page_config(
    page_title="Maize Disease Admin Dashboard",
    page_icon="🌽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CUSTOM_CSS + COMMUNITY_CSS, unsafe_allow_html=True)


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


def render_full_diagnosis_result(result: dict):
    if not result["valid"]:
        st.markdown(
            f'<div class="reject-panel"><h3>Image not accepted</h3><p>{result["message"]}</p></div>',
            unsafe_allow_html=True,
        )
        return

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


def render_shared_diagnosis_result(record: dict):
    if not record["valid"]:
        st.markdown(
            f'<div class="reject-panel"><h3>Image not accepted</h3><p>{record["message"]}</p></div>',
            unsafe_allow_html=True,
        )
        return

    color = DISEASE_COLORS.get(record["class_key"], "#3d6b4f")
    st.markdown(
        f"""
        <div class="result-panel" style="border-left-color: {color};">
            <div class="result-label">Predicted condition</div>
            <p class="result-disease">{record['display_name']}</p>
            <p class="result-scientific">{record['scientific_name']}</p>
            <p class="result-confidence">{record['confidence']:.1f}% <span>confidence</span></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**Class probabilities**")
    render_probability_bars(record["probabilities"], record["display_name"])

    st.markdown("**Description**")
    st.info(record["description"])
    with st.expander("Symptoms and management"):
        st.markdown(f"**Symptoms:** {record['symptoms']}")
        st.markdown(f"**Management:** {record['management']}")


def page_user_diagnosis():
    render_page_header(
        "User Diagnosis",
        "Latest uploads from the User Dashboard with full technical results.",
    )

    if st.button("Refresh"):
        st.rerun()

    records = load_user_diagnosis_batch()
    if not records:
        st.markdown(
            """
            <div class="empty-state">
                <p><strong>No user uploads yet</strong></p>
                <p>Upload maize leaf images on the User Dashboard.
                The images and full diagnoses will appear here automatically.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.caption(f"**{len(records)}** image(s) from the latest user upload batch")

    for index, record in enumerate(records, start=1):
        uploaded_at = record.get("timestamp", "Unknown time")
        filename = record.get("filename", f"image_{index}")
        st.markdown(f"### Image {index}: {filename}")
        st.caption(uploaded_at.replace("T", " ")[:19] + " UTC")

        col_image, col_result = st.columns([1, 1], gap="large")

        with col_image:
            st.markdown('<div class="panel"><div class="panel-title">Uploaded image</div>', unsafe_allow_html=True)
            st.image(str(record["image_path"]), caption="From User Dashboard", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_result:
            st.markdown('<div class="panel"><div class="panel-title">Full diagnosis</div>', unsafe_allow_html=True)
            render_shared_diagnosis_result(record)
            st.markdown("</div>", unsafe_allow_html=True)

        if index < len(records):
            st.markdown("---")


def render_admin_sidebar(model_path: str):
    st.sidebar.markdown(
        """
        <div class="sidebar-title">Admin Dashboard</div>
        <div class="sidebar-sub">Technical diagnosis and model evaluation</div>
        """,
        unsafe_allow_html=True,
    )

    page_label = st.sidebar.radio("Menu", list(PAGES.keys()), label_visibility="collapsed")
    page = PAGES[page_label]

    st.sidebar.markdown("---")
    st.sidebar.markdown("**System**")
    st.sidebar.caption("Model ready")
    st.sidebar.code(Path(model_path).name, language=None)

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

        image, _ = resolve_diagnosis_image(uploaded)

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
                    <p>Upload a maize leaf photograph from your device.<br>
                    Diagnosis runs as soon as an image is provided.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            with st.spinner("Analyzing image..."):
                result = predict_disease(model, image)

            render_full_diagnosis_result(result)

        st.markdown("</div>", unsafe_allow_html=True)


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
        - **Split:** 70% train / 15% validation / 15% test
        - **Deployment:** Streamlit web application
        """)
    with col2:
        st.markdown("### Disease classes")
        for cls in CLASS_NAMES:
            st.markdown(
                f"- **{DISPLAY_NAMES[cls]}** — *{SCIENTIFIC_NAMES[cls]}*"
            )

    st.markdown("---")
    st.markdown("""
    ### Dashboards
    - **User Dashboard** (`user_app.py`) — farmers upload a leaf and see management advice
    - **Admin Dashboard** (`app.py`) — **User Diagnosis** shows the latest user upload with full results """)
    



def main():
    try:
        model, model_path = autoload_resources()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.stop()

    page = render_admin_sidebar(model_path)

    if page == "user_diagnosis":
        page_user_diagnosis()
    elif page == "community":
        render_community_page("en", admin_view=True)
    elif page == "diagnose":
        page_diagnose(model)
    elif page == "performance":
        page_performance()
    else:
        page_about()


if __name__ == "__main__":
    ensure_streamlit(Path(__file__).resolve(), default_port=8502)

if streamlit_context_active():
    main()
