"""Stop all Streamlit dashboard processes for this project."""

from __future__ import annotations

import os
import re
import subprocess
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.name.lower()
MARKERS = (
    "user_app.py",
    "streamlit run app.py",
    'streamlit.exe" run app.py',
    "streamlit.exe run app.py",
    f"{PROJECT_DIR}\\app.py",
    f"{PROJECT_DIR}/app.py",
    f"{PROJECT_DIR}\\user_app.py",
    f"{PROJECT_DIR}/user_app.py",
)


def _list_python_processes() -> list[tuple[int, str]]:
    result = subprocess.run(
        ["wmic", "process", "where", "name='python.exe'", "get", "ProcessId,CommandLine"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    processes: list[tuple[int, str]] = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("CommandLine") or line.startswith("Node,"):
            continue
        match = re.search(r"(\d+)\s*$", line)
        if not match:
            continue
        pid = int(match.group(1))
        command = line[: match.start()].strip()
        processes.append((pid, command))
    return processes


def _should_stop(command: str) -> bool:
    command_lower = command.lower()
    if "stop_dashboards.py" in command_lower or "launch_both.py" in command_lower:
        return False
    if any(marker.lower() in command_lower for marker in MARKERS):
        return True
    return command_lower.rstrip().endswith("app.py") and "user_app.py" not in command_lower


def stop_dashboard_processes() -> list[int]:
    current_pid = os.getpid()
    killed: list[int] = []

    for pid, command in _list_python_processes():
        if pid == current_pid or not _should_stop(command):
            continue

        subprocess.run(
            ["taskkill", "/F", "/PID", str(pid)],
            capture_output=True,
            check=False,
        )
        killed.append(pid)

    return killed


def main() -> None:
    killed = stop_dashboard_processes()
    if killed:
        print(f"Stopped {len(killed)} old dashboard process(es): {', '.join(map(str, killed))}")
        time.sleep(2)
    else:
        print("No old dashboard processes found.")


if __name__ == "__main__":
    main()
