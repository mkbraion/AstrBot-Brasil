# Instalação — AstrBot Brasil

## Windows 10/11

Abra o PowerShell na pasta do projeto e execute:

```powershell
Set-Location -LiteralPath "C:\caminho\para\AstrBot Brasil"
.\install.ps1
.\start.ps1
```

Se a execução de scripts estiver bloqueada:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Depois feche e abra o PowerShell novamente.

## Instalação manual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

## Docker

```powershell
docker compose up -d
docker compose logs -f
```

## Segurança

Não salve API keys, tokens ou senhas em arquivos versionados. Antes de um commit, use `git status` e revise cuidadosamente os arquivos adicionados.
