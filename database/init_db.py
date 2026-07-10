"""Initialize the maize diagnosis SQLite database."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.db import init_database, get_diagnosis_stats

if __name__ == "__main__":
    path = init_database()
    stats = get_diagnosis_stats()
    print(f"Database ready: {path}")
    print(f"Records: {stats['total']} (accepted: {stats['accepted']}, rejected: {stats['rejected']})")
