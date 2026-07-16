Set-Location $PSScriptRoot
Write-Host "Starting User Dashboard..." -ForegroundColor Green
Write-Host "Opening http://localhost:8501" -ForegroundColor Cyan
python -m streamlit run user_app.py --server.port 8501
