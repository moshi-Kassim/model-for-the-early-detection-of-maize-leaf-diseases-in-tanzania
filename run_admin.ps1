Set-Location $PSScriptRoot
Write-Host "Starting Admin Dashboard..." -ForegroundColor Green
Write-Host "Opening http://localhost:8502" -ForegroundColor Cyan
python -m streamlit run app.py --server.port 8502
