# Solução de problemas — AstrBot Brasil

## A CLI não inicia

Confira:

```powershell
python --version
pip --version
```

O projeto requer Python 3.12 ou superior.

## Ambiente virtual não ativa

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Abra um novo PowerShell e execute:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Dependências com erro

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Dashboard em idioma incorreto

Selecione Português (Brasil) no seletor de idiomas. Se houver uma preferência antiga salva, troque o idioma uma vez pela interface para atualizar o `localStorage`.

## Antes de abrir uma Issue

Remova de logs qualquer API key, token, senha, cookie ou informação privada.
