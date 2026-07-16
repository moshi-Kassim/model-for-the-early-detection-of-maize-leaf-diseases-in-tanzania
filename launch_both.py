"""Stop old dashboards and launch User (8501) + Admin (8502) in new windows."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "stop_dashboards.py")], check=False)
    time.sleep(1)

    user_cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(ROOT / "user_app.py"),
        "--server.port",
        "8501",
    ]
    admin_cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(ROOT / "app.py"),
        "--server.port",
        "8502",
    ]

    creationflags = subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
    subprocess.Popen(user_cmd, cwd=ROOT, creationflags=creationflags)
    subprocess.Popen(admin_cmd, cwd=ROOT, creationflags=creationflags)

    print("User Dashboard:  http://localhost:8501")
    print("Admin Dashboard: http://localhost:8502")


if __name__ == "__main__":
    main()
