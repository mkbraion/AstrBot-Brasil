$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
Write-Host 'Iniciando AstrBot Brasil...' -ForegroundColor Cyan
if (-not (Test-Path '.venv\Scripts\python.exe')) {
    Write-Host 'Ambiente virtual não encontrado. Execute .\install.ps1 primeiro.' -ForegroundColor Yellow
    exit 1
}
if (-not (Test-Path 'dashboard/dist/index.html')) {
    Write-Host 'Compile o painel traduzido com .\build-dashboard.ps1 antes de iniciar.' -ForegroundColor Yellow
    exit 1
}
& .\.venv\Scripts\python.exe .\main.py --webui-dir .\dashboard\dist
exit $LASTEXITCODE
