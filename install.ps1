$ErrorActionPreference = 'Stop'
Write-Host 'AstrBot Brasil - Instalador para Windows' -ForegroundColor Cyan
Write-Host 'Verificando Python...'
python --version
if (-not (Test-Path '.venv')) {
    Write-Host 'Criando ambiente virtual...'
    python -m venv .venv
}
Write-Host 'Ativando ambiente virtual...'
& .\.venv\Scripts\Activate.ps1
Write-Host 'Atualizando pip...'
python -m pip install --upgrade pip
Write-Host 'Instalando dependências...'
pip install -r requirements.txt
Write-Host 'Instalação concluída. Execute .\start.ps1 para iniciar o AstrBot Brasil.' -ForegroundColor Green
