@echo off
title Maize Leaf Disease Dashboard
cd /d "%~dp0"
echo Starting Maize Disease Dashboard...
echo Browser will open automatically at http://localhost:8501
python -m streamlit run app.py
pause
