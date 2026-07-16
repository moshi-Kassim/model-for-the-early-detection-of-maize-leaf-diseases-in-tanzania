@echo off
title Maize Leaf Care - User Dashboard
cd /d "%~dp0"
python stop_dashboards.py
echo Starting User Dashboard on http://localhost:8501
start "User Dashboard (8501)" cmd /k python -m streamlit run user_app.py --server.port 8501
