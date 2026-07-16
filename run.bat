@echo off
title Maize Leaf Care - User Dashboard
cd /d "%~dp0"
echo Starting User Dashboard...
echo Browser will open at http://localhost:8501
python -m streamlit run user_app.py --server.port 8501
pause
