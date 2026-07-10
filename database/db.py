"""SQLite database for maize leaf diagnosis records."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "maize_diagnosis.db"
UPLOADS_DIR = DB_DIR / "uploads"

SCHEMA = """
CREATE TABLE IF NOT EXISTS diagnoses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    image_filename TEXT,
    image_path TEXT,
    predicted_class TEXT,
    display_name TEXT,
    confidence REAL,
    status TEXT NOT NULL CHECK (status IN ('accepted', 'rejected')),
    rejection_reason TEXT,
    probabilities_json TEXT,
    source TEXT NOT NULL DEFAULT 'upload',
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_diagnoses_created_at ON diagnoses(created_at);
CREATE INDEX IF NOT EXISTS idx_diagnoses_status ON diagnoses(status);
CREATE INDEX IF NOT EXISTS idx_diagnoses_predicted_class ON diagnoses(predicted_class);
"""


def init_database(db_path: Path | None = None) -> Path:
    """Create database file, tables, and uploads folder if missing."""
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(path) as conn:
        conn.executescript(SCHEMA)
        conn.commit()
    return path


@contextmanager
def get_connection(db_path: Path | None = None):
    path = init_database(db_path)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def save_diagnosis(
    *,
    status: str,
    source: str = "upload",
    image_filename: str | None = None,
    image_path: str | None = None,
    predicted_class: str | None = None,
    display_name: str | None = None,
    confidence: float | None = None,
    rejection_reason: str | None = None,
    probabilities: dict[str, float] | None = None,
    notes: str | None = None,
) -> int:
    """Insert a diagnosis record and return its id."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO diagnoses (
                created_at, image_filename, image_path, predicted_class, display_name,
                confidence, status, rejection_reason, probabilities_json, source, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                _utc_now(),
                image_filename,
                image_path,
                predicted_class,
                display_name,
                confidence,
                status,
                rejection_reason,
                json.dumps(probabilities) if probabilities else None,
                source,
                notes,
            ),
        )
        return int(cursor.lastrowid)


def get_all_diagnoses(limit: int = 200) -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM diagnoses
            ORDER BY datetime(created_at) DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def get_diagnosis_stats() -> dict[str, Any]:
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM diagnoses").fetchone()[0]
        accepted = conn.execute(
            "SELECT COUNT(*) FROM diagnoses WHERE status = 'accepted'"
        ).fetchone()[0]
        rejected = conn.execute(
            "SELECT COUNT(*) FROM diagnoses WHERE status = 'rejected'"
        ).fetchone()[0]
        by_class = conn.execute(
            """
            SELECT display_name, COUNT(*) AS count
            FROM diagnoses
            WHERE status = 'accepted' AND display_name IS NOT NULL
            GROUP BY display_name
            ORDER BY count DESC
            """
        ).fetchall()
    return {
        "total": total,
        "accepted": accepted,
        "rejected": rejected,
        "by_class": {row["display_name"]: row["count"] for row in by_class},
    }


def clear_all_diagnoses() -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM diagnoses")


def save_uploaded_image(image_bytes: bytes, filename: str) -> str:
    """Save uploaded image copy and return stored path."""
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = Path(filename).name
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    stored_name = f"{timestamp}_{safe_name}"
    stored_path = UPLOADS_DIR / stored_name
    stored_path.write_bytes(image_bytes)
    return str(stored_path)
