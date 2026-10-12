$ErrorActionPreference = 'Stop'
Write-Host 'Iniciando AstrBot Brasil...' -ForegroundColor Cyan
if (-not (Test-Path '.venv\Scripts\python.exe')) {
    Write-Host 'Ambiente virtual não encontrado. Execute .\install.ps1 primeiro.' -ForegroundColor Yellow
    exit 1
}
& .\.venv\Scripts\python.exe .\main.py
