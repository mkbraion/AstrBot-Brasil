# Instalação — AstrBot Brasil

## Windows 10/11

Instale Python 3.12 ou superior e Node.js 20 ou superior com npm. O pnpm é opcional: o script usa a versão 10.32.1 do pnpm para compilar e verificar o painel brasileiro antes de concluir.

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
./build-dashboard.ps1
python main.py --webui-dir dashboard/dist
```

## Docker

O Docker compila o painel e o núcleo a partir deste repositório e cria a imagem local `astrbot-brasil:local`. Não é necessário instalar Python ou Node.js na máquina ao usar esta opção.

```powershell
docker compose up -d --build
docker compose logs -f
```

## Segurança

Não salve API keys, tokens ou senhas em arquivos versionados. Antes de um commit, use `git status` e revise cuidadosamente os arquivos adicionados.

## Painel em português

Para recompilar depois de atualizar o código, execute `./build-dashboard.ps1` e reinicie com `./start.ps1`. O script usa pnpm 10.32.1, verifica os idiomas, compila e registra a versão do núcleo em `dashboard/dist/assets/version`.

No Linux ou macOS, execute `pnpm install --frozen-lockfile`, `pnpm run i18n:check`, `pnpm run i18n:check:ptbr` e `pnpm run build` dentro de `dashboard/`. Na raiz do projeto, registre a versão com `python -c "from pathlib import Path; from astrbot import __version__; Path('dashboard/dist/assets/version').write_text('v' + __version__, encoding='utf-8')"` e inicie com `python main.py --webui-dir dashboard/dist`.

A interface e os fluxos internos de usuário foram localizados. Nomes de serviços, identificadores técnicos e valores exigidos por APIs são preservados. Logs de desenvolvimento, comentários do código, documentação original e conteúdos de plugins ou serviços externos podem usar o idioma original.
