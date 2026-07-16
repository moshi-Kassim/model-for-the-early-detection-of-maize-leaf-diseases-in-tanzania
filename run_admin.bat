@echo off
title Maize Disease Admin Dashboard
cd /d "%~dp0"
python stop_dashboards.py
echo Starting Admin Dashboard on http://localhost:8502
start "Admin Dashboard (8502)" cmd /k python -m streamlit run app.py --server.port 8502
