"""Share user-dashboard diagnoses with the admin dashboard."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
SHARED_DIR = BASE_DIR / "shared"
BATCH_DIR = SHARED_DIR / "batch"
BATCH_JSON = SHARED_DIR / "user_batch.json"
LATEST_IMAGE = SHARED_DIR / "latest_image.jpg"
LATEST_JSON = SHARED_DIR / "latest_diagnosis.json"


def _result_payload(result: dict, *, filename: str, image_file: str) -> dict:
    payload = {
        "filename": filename,
        "image_file": image_file,
        "valid": result["valid"],
    }
    if result["valid"]:
        payload.update(
            {
                "class_key": result["class_key"],
                "display_name": result["display_name"],
                "scientific_name": result["scientific_name"],
                "confidence": result["confidence"],
                "probabilities": result["probabilities"],
                "description": result["info"]["description"],
                "symptoms": result["info"]["symptoms"],
                "management": result["info"]["management"],
            }
        )
    else:
        payload["message"] = result["message"]
    return payload


def save_user_diagnosis_batch(items: list[tuple[Image.Image, dict, str]]) -> None:
    """Save a batch of user uploads for the admin dashboard."""
    SHARED_DIR.mkdir(parents=True, exist_ok=True)
    if BATCH_DIR.exists():
        shutil.rmtree(BATCH_DIR)
    BATCH_DIR.mkdir(parents=True, exist_ok=True)

    records = []
    for index, (image, result, filename) in enumerate(items):
        image_name = f"image_{index}.jpg"
        image_path = BATCH_DIR / image_name
        image.convert("RGB").save(image_path, format="JPEG", quality=90)
        records.append(_result_payload(result, filename=filename, image_file=image_name))

    batch = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "user_dashboard",
        "count": len(records),
        "items": records,
    }
    BATCH_JSON.write_text(json.dumps(batch, indent=2), encoding="utf-8")

    if items:
        save_user_diagnosis(items[-1][0], items[-1][1], filename=items[-1][2])


def save_user_diagnosis(image: Image.Image, result: dict, *, filename: str = "upload") -> None:
    """Keep the latest single diagnosis for backward compatibility."""
    SHARED_DIR.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(LATEST_IMAGE, format="JPEG", quality=90)

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "user_dashboard",
        "filename": filename,
        "valid": result["valid"],
    }

    if result["valid"]:
        payload.update(
            {
                "class_key": result["class_key"],
                "display_name": result["display_name"],
                "scientific_name": result["scientific_name"],
                "confidence": result["confidence"],
                "probabilities": result["probabilities"],
                "description": result["info"]["description"],
                "symptoms": result["info"]["symptoms"],
                "management": result["info"]["management"],
            }
        )
    else:
        payload["message"] = result["message"]

    LATEST_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_user_diagnosis_batch() -> list[dict]:
    if not BATCH_JSON.exists() or not BATCH_DIR.exists():
        latest = load_latest_diagnosis()
        return [latest] if latest else []

    batch = json.loads(BATCH_JSON.read_text(encoding="utf-8"))
    records = []
    for item in batch.get("items", []):
        record = dict(item)
        record["timestamp"] = batch.get("timestamp")
        record["image_path"] = BATCH_DIR / item["image_file"]
        records.append(record)
    return records


def load_latest_diagnosis() -> dict | None:
    if not LATEST_JSON.exists() or not LATEST_IMAGE.exists():
        return None

    data = json.loads(LATEST_JSON.read_text(encoding="utf-8"))
    data["image_path"] = LATEST_IMAGE
    return data
