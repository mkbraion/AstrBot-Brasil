$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
Write-Host 'AstrBot Brasil - Instalador para Windows' -ForegroundColor Cyan
Write-Host 'Verificando Python...'
python -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)"
if ($LASTEXITCODE -ne 0) { throw 'Instale Python 3.12 ou superior antes de continuar.' }
if (-not (Test-Path '.venv')) {
    Write-Host 'Criando ambiente virtual...'
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao criar o ambiente Python.' }
}
$venvPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $venvPython -PathType Leaf)) {
    throw 'O ambiente .venv está incompleto. Crie um ambiente com Python 3.12 ou superior.'
}
& $venvPython -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)"
if ($LASTEXITCODE -ne 0) { throw 'O ambiente .venv precisa usar Python 3.12 ou superior.' }
Write-Host 'Atualizando pip...'
& $venvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw 'Falha ao atualizar o pip.' }
Write-Host 'Instalando dependências...'
& $venvPython -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar as dependências Python.' }
& (Join-Path $PSScriptRoot 'build-dashboard.ps1')
Write-Host 'Instalação concluída. Execute .\start.ps1 para iniciar o AstrBot Brasil.' -ForegroundColor Green
