"""Farmer-facing user dashboard — upload, top disease result, and management only."""

import io
from pathlib import Path

import streamlit as st
from PIL import Image

from utils.community_ui import COMMUNITY_CSS, render_community_page, render_help_request_form
from utils.dashboard_core import (
    autoload_resources,
    ensure_streamlit,
    predict_disease,
    render_page_header,
    streamlit_context_active,
)
from utils.shared_diagnosis import save_user_diagnosis_batch
from utils.theme import CUSTOM_CSS, DISEASE_COLORS
from utils.translations import LANGUAGES, localize_disease, t, translate_rejection

USER_PAGES = {
    "Diagnose": "diagnose",
    "Community Help": "community",
}

USER_PAGE_CSS = """
<style>
    section.main div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(180deg, #ffffff 0%, #f4fbf5 100%);
        border: 1px solid #c5dfc9 !important;
        border-top: 3px solid #3d6b4f !important;
        border-radius: 16px !important;
        min-height: 480px;
        padding: 0.5rem 0.65rem 0.85rem;
        box-shadow:
            0 4px 6px rgba(45, 90, 61, 0.06),
            0 12px 28px rgba(45, 90, 61, 0.12);
    }
    section.main .user-panel-heading {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        color: #2d5a3d;
        margin: 0.25rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #c5dfc9;
    }
    section.main div[data-testid="stFileUploader"] {
        border: 1px dashed #8fbf9a;
        border-radius: 12px;
        background: linear-gradient(180deg, #f8fbf8 0%, #eef8f0 100%);
        box-shadow: inset 0 1px 3px rgba(45, 90, 61, 0.06);
    }
    section.main .empty-state {
        min-height: 320px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .user-result-card {
        border: 1px solid #c5dfc9;
        border-left: 4px solid #3d6b4f;
        border-radius: 14px;
        padding: 0.95rem 1rem;
        margin-bottom: 0.95rem;
        background: linear-gradient(135deg, #ffffff 0%, #f4fbf5 100%);
        box-shadow:
            0 3px 8px rgba(45, 90, 61, 0.07),
            0 8px 20px rgba(45, 90, 61, 0.09);
    }
    .user-result-card:last-child {
        margin-bottom: 0;
    }
    .user-result-card:hover {
        box-shadow:
            0 6px 14px rgba(21, 37, 21, 0.07),
            0 14px 30px rgba(21, 37, 21, 0.10);
    }
    .user-result-filename {
        font-size: 0.82rem;
        font-weight: 600;
        color: #374151;
        margin: 0 0 0.65rem 0;
    }
    .user-grid-gap {
        margin-top: 0.5rem;
    }
</style>
"""

st.set_page_config(
    page_title="Maize Leaf Care",
    page_icon="🌽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CUSTOM_CSS + USER_PAGE_CSS + COMMUNITY_CSS, unsafe_allow_html=True)


def get_language() -> str:
    if "user_language" not in st.session_state:
        st.session_state.user_language = "en"
    return st.session_state.user_language


def render_user_sidebar(lang: str) -> str:
    st.sidebar.markdown(
        f"""
        <div class="sidebar-title">{t("sidebar_title", lang)}</div>
        <div class="sidebar-sub">{t("sidebar_sub", lang)}</div>
        """,
        unsafe_allow_html=True,
    )

    selected = st.sidebar.selectbox(
        t("language_label", lang),
        options=list(LANGUAGES.keys()),
        format_func=lambda code: LANGUAGES[code],
        index=list(LANGUAGES.keys()).index(get_language()),
        key="language_selector",
    )
    if selected != st.session_state.user_language:
        st.session_state.user_language = selected
        st.rerun()

    page_labels = {t("nav_diagnose", lang): "diagnose", t("nav_community", lang): "community"}
    page_label = st.sidebar.radio(
        "Menu",
        list(page_labels.keys()),
        label_visibility="collapsed",
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**{t('how_to_use_title', lang)}**")
    st.sidebar.markdown(t("how_to_use_steps", lang))
    st.sidebar.caption(t("sidebar_note", lang))

    return page_labels[page_label]


def render_single_result(result: dict, lang: str, *, filename: str | None = None):
    if filename:
        st.markdown(
            f'<p class="user-result-filename">{t("result_for", lang)}: {filename}</p>',
            unsafe_allow_html=True,
        )

    if not result["valid"]:
        rejection = translate_rejection(result["message"], lang)
        st.markdown(
            f'<div class="reject-panel"><h3>{t("reject_title", lang)}</h3><p>{rejection}</p></div>',
            unsafe_allow_html=True,
        )
        return

    localized = localize_disease(result["class_key"], lang)
    color = DISEASE_COLORS.get(result["class_key"], "#3d6b4f")
    st.markdown(
        f"""
        <div class="user-badge">{t("top_prediction", lang)}</div>
        <div class="result-panel" style="border-left-color: {color};">
            <div class="result-label">{t("detected_condition", lang)}</div>
            <p class="result-disease">{localized["display_name"]}</p>
            <p class="result-scientific">{result["scientific_name"]}</p>
            <p class="result-confidence">{result['confidence']:.1f}% <span>{t("confidence", lang)}</span></p>
        </div>
        <div class="management-panel">
            <h3>{t("recommended_management", lang)}</h3>
            <p>{localized["management"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def process_uploads(model, uploaded_files, lang: str):
    items = []
    total = len(uploaded_files)

    for index, uploaded in enumerate(uploaded_files, start=1):
        with st.spinner(t("analyzing_one", lang, current=index, total=total)):
            image = Image.open(io.BytesIO(uploaded.getvalue()))
            result = predict_disease(model, image)
            items.append((image, result, uploaded.name))

    save_user_diagnosis_batch(items)
    return items


def page_diagnose(model, lang: str):
    render_page_header(
        t("dashboard_title", lang),
        t("dashboard_subtitle", lang),
    )

    col_upload, col_result = st.columns(2, gap="large")

    with col_upload:
        with st.container(border=True):
            st.markdown(
                f'<div class="user-panel-heading">{t("upload_panel_title", lang)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="notice">{t("upload_notice", lang)}</div>',
                unsafe_allow_html=True,
            )
            uploaded_files = st.file_uploader(
                t("upload_panel_title", lang),
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
                label_visibility="collapsed",
                key="user_upload",
                help=t("upload_help", lang),
            )

            if uploaded_files:
                st.caption(t("images_selected", lang, count=len(uploaded_files)))
                preview_cols = st.columns(min(len(uploaded_files), 3))
                for index, uploaded in enumerate(uploaded_files):
                    with preview_cols[index % len(preview_cols)]:
                        image = Image.open(io.BytesIO(uploaded.getvalue()))
                        st.image(image, caption=uploaded.name, use_container_width=True)

    diagnosis_items = []
    with col_result:
        with st.container(border=True):
            st.markdown(
                f'<div class="user-panel-heading">{t("result_panel_title", lang)}</div>',
                unsafe_allow_html=True,
            )

            if not uploaded_files:
                st.markdown(
                    f"""
                    <div class="empty-state">
                        <p><strong>{t("empty_title", lang)}</strong></p>
                        <p>{t("empty_body", lang)}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                diagnosis_items = process_uploads(model, uploaded_files, lang)
                for image, result, filename in diagnosis_items:
                    st.markdown('<div class="user-result-card">', unsafe_allow_html=True)
                    thumb_col, text_col = st.columns([1, 2], gap="small")
                    with thumb_col:
                        st.image(image, use_container_width=True)
                    with text_col:
                        render_single_result(result, lang, filename=filename)
                    st.markdown("</div>", unsafe_allow_html=True)

    if diagnosis_items:
        render_help_request_form(diagnosis_items, lang)


def main():
    lang = get_language()
    page = render_user_sidebar(lang)

    try:
        model, _ = autoload_resources()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.stop()

    if page == "community":
        render_community_page(lang)
    else:
        page_diagnose(model, lang)


if __name__ == "__main__":
    ensure_streamlit(Path(__file__).resolve(), default_port=8501)

if streamlit_context_active():
    main()
