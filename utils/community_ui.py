"""Shared UI for community help posts and replies."""

from __future__ import annotations

from pathlib import Path

import streamlit as st
from PIL import Image

from utils.community import (
    add_reply,
    create_post,
    delete_post,
    delete_reply,
    list_posts,
    list_replies,
    resolve_image_path,
)
from utils.translations import t

COMMUNITY_CSS = """
<style>
    .community-card {
        background: linear-gradient(135deg, #ffffff 0%, #f4fbf5 100%);
        border: 1px solid #c5dfc9;
        border-left: 4px solid #3d6b4f;
        border-radius: 14px;
        padding: 1.1rem 1.25rem;
        margin-bottom: 1rem;
        box-shadow:
            0 4px 6px rgba(21, 37, 21, 0.04),
            0 10px 24px rgba(21, 37, 21, 0.08);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .community-card:hover {
        transform: translateY(-2px);
        box-shadow:
            0 6px 12px rgba(21, 37, 21, 0.06),
            0 16px 32px rgba(21, 37, 21, 0.10);
    }
    .community-meta {
        font-size: 0.82rem;
        color: #6b7280;
        margin-bottom: 0.65rem;
    }
    .community-phone {
        display: inline-block;
        background: linear-gradient(135deg, rgba(61, 107, 79, 0.18) 0%, rgba(82, 183, 136, 0.15) 100%);
        color: #1a3d2a;
        border: 1px solid rgba(61, 107, 79, 0.25);
        border-radius: 999px;
        padding: 0.2rem 0.65rem;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 0.55rem;
    }
    .reply-box {
        background: #f8fbf8;
        border-left: 3px solid #3d6b4f;
        border-radius: 8px;
        padding: 0.75rem 0.9rem;
        margin-top: 0.55rem;
        box-shadow: inset 0 1px 2px rgba(21, 37, 21, 0.04);
    }
    .reply-box p {
        margin: 0.15rem 0;
        font-size: 0.9rem;
        color: #374151;
    }
    .reply-box-admin {
        background: #eef6f0;
        border-left: 3px solid #2d5a3d;
        box-shadow:
            inset 0 1px 2px rgba(21, 37, 21, 0.04),
            0 2px 8px rgba(45, 90, 61, 0.08);
    }
    .admin-badge {
        display: inline-block;
        background: #2d5a3d;
        color: #ffffff;
        border-radius: 999px;
        padding: 0.15rem 0.55rem;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }
    .help-form-panel {
        background: linear-gradient(180deg, #ffffff 0%, #eef8f0 100%);
        border: 1px solid #c5dfc9;
        border-left: 4px solid #52b788;
        border-radius: 14px;
        padding: 1rem 1.15rem;
        margin-top: 1rem;
        box-shadow: 0 8px 24px rgba(21, 37, 21, 0.08);
    }
</style>
"""


def render_help_request_form(
    diagnosis_items: list[tuple[Image.Image, dict, str]],
    lang: str,
) -> None:
    valid_items = [
        (image, result, filename)
        for image, result, filename in diagnosis_items
        if result.get("valid")
    ]
    if not valid_items:
        return

    st.markdown(
        f'<div class="help-form-panel"><div class="user-panel-heading">{t("help_request_title", lang)}</div>',
        unsafe_allow_html=True,
    )
    st.caption(t("help_request_subtitle", lang))

    labels = [filename for _, _, filename in valid_items]
    selected = st.selectbox(
        t("help_select_image", lang),
        options=range(len(valid_items)),
        format_func=lambda i: labels[i],
        key="help_selected_image",
    )
    phone = st.text_input(t("help_phone_label", lang), placeholder="+255...")
    comment = st.text_area(
        t("help_comment_label", lang),
        placeholder=t("help_comment_placeholder", lang),
        height=100,
    )

    if st.button(t("help_submit", lang), type="primary", use_container_width=True):
        if not phone.strip():
            st.warning(t("help_phone_required", lang))
        elif not comment.strip():
            st.warning(t("help_comment_required", lang))
        else:
            image, result, _ = valid_items[selected]
            create_post(
                phone=phone,
                comment=comment,
                image=image,
                disease_label=result["display_name"],
                confidence=result["confidence"],
                language=lang,
            )
            st.success(t("help_submit_success", lang))
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def _reply_author_label(reply: dict, lang: str) -> str:
    if reply.get("is_admin"):
        return t("help_admin_label", lang)
    return reply.get("phone") or ""


def _render_reply(reply: dict, lang: str, *, key_prefix: str, admin_view: bool) -> None:
    reply_time = reply.get("created_at", "")[:19].replace("T", " ")
    is_admin = bool(reply.get("is_admin"))
    author = _reply_author_label(reply, lang)
    box_class = "reply-box reply-box-admin" if is_admin else "reply-box"
    badge = (
        f'<span class="admin-badge">{t("help_admin_label", lang)}</span>'
        if is_admin
        else f"<strong>{author}</strong>"
    )
    st.markdown(
        f"""
        <div class="{box_class}">
            <p>{badge} · {reply_time}</p>
            <p>{reply["reply_text"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if admin_view:
        if st.button(
            t("help_delete_reply", lang),
            key=f"{key_prefix}_delete_reply_{reply['id']}",
            use_container_width=True,
        ):
            delete_reply(reply["id"])
            st.success(t("help_delete_success", lang))
            st.rerun()


def render_post_card(post: dict, lang: str, *, key_prefix: str, admin_view: bool = False) -> None:
    created = post.get("created_at", "")[:19].replace("T", " ")
    phone = post.get("phone") or ""

    st.markdown('<div class="community-card">', unsafe_allow_html=True)

    col_img, col_body = st.columns([1, 2], gap="medium")
    with col_img:
        image_path = resolve_image_path(post.get("image_path", ""))
        if image_path:
            st.image(str(image_path), use_container_width=True)

    with col_body:
        if admin_view:
            del_col, _ = st.columns([1, 3])
            with del_col:
                if st.button(
                    t("help_delete_post", lang),
                    key=f"{key_prefix}_delete_post_{post['id']}",
                    type="secondary",
                    use_container_width=True,
                ):
                    delete_post(post["id"])
                    st.success(t("help_delete_success", lang))
                    st.rerun()

        st.markdown(f'<div class="community-phone">{phone}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="community-meta">{t("help_posted", lang)}: {created}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(post["comment"])

        replies = list_replies(post["id"])
        if replies:
            st.markdown(f"**{t('help_replies', lang)} ({len(replies)})**")
            for reply in replies:
                _render_reply(reply, lang, key_prefix=key_prefix, admin_view=admin_view)

        if admin_view:
            with st.expander(t("help_admin_reply_action", lang)):
                reply_text = st.text_area(
                    t("help_reply_text", lang),
                    key=f"{key_prefix}_admin_reply_text_{post['id']}",
                    height=100,
                )
                if st.button(
                    t("help_reply_submit", lang),
                    key=f"{key_prefix}_admin_reply_submit_{post['id']}",
                    type="primary",
                    use_container_width=True,
                ):
                    if not reply_text.strip():
                        st.warning(t("help_comment_required", lang))
                    else:
                        add_reply(
                            post_id=post["id"],
                            reply_text=reply_text,
                            is_admin=True,
                        )
                        st.success(t("help_admin_reply_success", lang))
                        st.rerun()
        else:
            with st.expander(t("help_reply_action", lang)):
                reply_phone = st.text_input(
                    t("help_reply_phone", lang),
                    placeholder="+255...",
                    key=f"{key_prefix}_reply_phone_{post['id']}",
                )
                reply_text = st.text_area(
                    t("help_reply_text", lang),
                    key=f"{key_prefix}_reply_text_{post['id']}",
                    height=80,
                )
                if st.button(
                    t("help_reply_submit", lang),
                    key=f"{key_prefix}_reply_submit_{post['id']}",
                    use_container_width=True,
                ):
                    if not reply_phone.strip():
                        st.warning(t("help_phone_required", lang))
                    elif not reply_text.strip():
                        st.warning(t("help_comment_required", lang))
                    else:
                        add_reply(
                            post_id=post["id"],
                            phone=reply_phone,
                            reply_text=reply_text,
                        )
                        st.success(t("help_reply_success", lang))
                        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_community_page(lang: str, *, admin_view: bool = False) -> None:
    from utils.dashboard_core import render_page_header

    title = t("community_admin_title", lang) if admin_view else t("community_title", lang)
    subtitle = t("community_admin_subtitle", lang) if admin_view else t("community_subtitle", lang)
    render_page_header(title, subtitle)

    if admin_view and st.button("Refresh", key="community_admin_refresh"):
        st.rerun()

    posts = list_posts()
    if not posts:
        st.markdown(
            f"""
            <div class="empty-state">
                <p><strong>{t("community_empty_title", lang)}</strong></p>
                <p>{t("community_empty_body", lang)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.caption(t("community_count", lang, count=len(posts)))
    prefix = "admin" if admin_view else "user"
    for post in posts:
        render_post_card(post, lang, key_prefix=prefix, admin_view=admin_view)
