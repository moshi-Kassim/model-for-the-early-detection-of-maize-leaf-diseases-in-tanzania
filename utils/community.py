"""Community help requests — farmers ask questions; others can reply."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "community.db"
IMAGES_DIR = BASE_DIR / "data" / "community_images"


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
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

    image_path = IMAGES_DIR / f"post_{post_id}.jpg"
    image.convert("RGB").save(image_path, format="JPEG", quality=90)

    with _connect() as conn:
        conn.execute(
            "UPDATE posts SET image_path = ? WHERE id = ?",
            (str(image_path), post_id),
        )

    return post_id


def list_posts() -> list[dict]:
    init_db()
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM posts ORDER BY datetime(created_at) DESC"
        ).fetchall()
    return [dict(row) for row in rows]


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
        return int(cursor.lastrowid)


def delete_post(post_id: int) -> bool:
    init_db()
    with _connect() as conn:
        row = conn.execute(
            "SELECT image_path FROM posts WHERE id = ?",
            (post_id,),
        ).fetchone()
        if row is None:
            return False
        image_path = Path(row["image_path"])
        conn.execute("DELETE FROM replies WHERE post_id = ?", (post_id,))
        conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    if image_path and image_path.exists():
        image_path.unlink(missing_ok=True)
    return True


def delete_reply(reply_id: int) -> bool:
    init_db()
    with _connect() as conn:
        cursor = conn.execute("DELETE FROM replies WHERE id = ?", (reply_id,))
        return cursor.rowcount > 0
