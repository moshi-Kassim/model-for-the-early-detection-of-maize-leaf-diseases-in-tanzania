Set-Location $PSScriptRoot
Write-Host "Starting Maize Disease Dashboard..." -ForegroundColor Green
Write-Host "Opening http://localhost:8501" -ForegroundColor Cyan
python -m streamlit run app.py
