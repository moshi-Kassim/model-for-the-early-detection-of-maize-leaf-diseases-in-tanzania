"""Community help requests — farmers ask questions; others can reply."""

from __future__ import annotations

import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
SHARED_DIR = BASE_DIR / "shared"
DB_PATH = SHARED_DIR / "community.db"
IMAGES_DIR = SHARED_DIR / "community_images"
EXPORT_JSON = SHARED_DIR / "community_posts.json"
LEGACY_DB_PATH = BASE_DIR / "data" / "community.db"
LEGACY_IMAGES_DIR = BASE_DIR / "data" / "community_images"


def _connect() -> sqlite3.Connection:
    SHARED_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _migrate_legacy_storage() -> None:
    """Move old community data from data/ into shared/ (once)."""
    SHARED_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    if LEGACY_DB_PATH.exists() and not DB_PATH.exists():
        shutil.copy2(LEGACY_DB_PATH, DB_PATH)

    if LEGACY_IMAGES_DIR.exists():
        for image in LEGACY_IMAGES_DIR.glob("*.jpg"):
            target = IMAGES_DIR / image.name
            if not target.exists():
                shutil.copy2(image, target)


def init_db() -> None:
    _migrate_legacy_storage()
    with _connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                phone TEXT NOT NULL,
                comment TEXT NOT NULL,
                image_path TEXT NOT NULL,
                disease_label TEXT,
                confidence REAL,
                language TEXT DEFAULT 'en'
            );

            CREATE TABLE IF NOT EXISTS replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                phone TEXT NOT NULL,
                reply_text TEXT NOT NULL,
                is_admin INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (post_id) REFERENCES posts(id)
            );
            """
        )
        columns = {
            row[1] for row in conn.execute("PRAGMA table_info(replies)").fetchall()
        }
        if "is_admin" not in columns:
            conn.execute(
                "ALTER TABLE replies ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0"
            )

    if DB_PATH.exists() and not EXPORT_JSON.exists():
        _export_posts_json()


def resolve_image_path(stored_path: str) -> Path | None:
    """Find a post image whether the DB stores a relative or legacy absolute path."""
    if not stored_path:
        return None

    path = Path(stored_path)
    candidates = [
        path,
        IMAGES_DIR / path.name,
        SHARED_DIR / path,
        BASE_DIR / path,
        LEGACY_IMAGES_DIR / path.name,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _export_posts_json() -> None:
    """Export posts for the admin dashboard (same pattern as user diagnosis sync)."""
    posts = []
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM posts ORDER BY datetime(created_at) DESC"
        ).fetchall()
        for row in rows:
            post = dict(row)
            image_path = resolve_image_path(post.get("image_path", ""))
            post["image_file"] = image_path.name if image_path else Path(post["image_path"]).name
            post["replies"] = [
                dict(reply)
                for reply in conn.execute(
                    "SELECT * FROM replies WHERE post_id = ? ORDER BY datetime(created_at) ASC",
                    (post["id"],),
                ).fetchall()
            ]
            posts.append(post)

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "community_help",
        "count": len(posts),
        "items": posts,
    }
    EXPORT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def create_post(
    *,
    phone: str,
    comment: str,
    image: Image.Image,
    disease_label: str | None = None,
    confidence: float | None = None,
    language: str = "en",
) -> int:
    init_db()
    created_at = datetime.now(timezone.utc).isoformat()

    with _connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO posts (created_at, phone, comment, image_path, disease_label, confidence, language)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (created_at, phone.strip(), comment.strip(), "", disease_label, confidence, language),
        )
        post_id = int(cursor.lastrowid)

    image_name = f"post_{post_id}.jpg"
    image_path = IMAGES_DIR / image_name
    image.convert("RGB").save(image_path, format="JPEG", quality=90)

    with _connect() as conn:
        conn.execute(
            "UPDATE posts SET image_path = ? WHERE id = ?",
            (image_name, post_id),
        )

    _export_posts_json()
    return post_id


def list_posts() -> list[dict]:
    init_db()
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM posts ORDER BY datetime(created_at) DESC"
        ).fetchall()

    posts = []
    for row in rows:
        post = dict(row)
        resolved = resolve_image_path(post.get("image_path", ""))
        if resolved:
            post["image_path"] = str(resolved)
        posts.append(post)
    return posts


def list_replies(post_id: int) -> list[dict]:
    init_db()
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM replies WHERE post_id = ? ORDER BY datetime(created_at) ASC",
            (post_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def add_reply(
    *,
    post_id: int,
    reply_text: str,
    phone: str = "",
    is_admin: bool = False,
) -> int:
    init_db()
    created_at = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO replies (post_id, created_at, phone, reply_text, is_admin)
            VALUES (?, ?, ?, ?, ?)
            """,
            (post_id, created_at, phone.strip(), reply_text.strip(), int(is_admin)),
        )
        reply_id = int(cursor.lastrowid)

    _export_posts_json()
    return reply_id


def delete_post(post_id: int) -> bool:
    init_db()
    with _connect() as conn:
        row = conn.execute(
            "SELECT image_path FROM posts WHERE id = ?",
            (post_id,),
        ).fetchone()
        if row is None:
            return False
        image_path = resolve_image_path(row["image_path"])
        conn.execute("DELETE FROM replies WHERE post_id = ?", (post_id,))
        conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))

    if image_path and image_path.exists():
        image_path.unlink(missing_ok=True)

    _export_posts_json()
    return True


def delete_reply(reply_id: int) -> bool:
    init_db()
    with _connect() as conn:
        cursor = conn.execute("DELETE FROM replies WHERE id = ?", (reply_id,))
        deleted = cursor.rowcount > 0

    if deleted:
        _export_posts_json()
    return deleted
