<!-- MKBRAION-POLISH:START -->
<div align="center">

# Astrbot Brasil

**Plataforma de chatbot e automação com IA adaptada para português do Brasil, com foco em comunidade, extensibilidade e experiência brasileira.**

[![Repositório](https://img.shields.io/badge/GitHub-Repositório-181717?logo=github)](https://github.com/mkbraion/AstrBot-Brasil)

</div>

**Stack / tópicos:** ``artificial-intelligence`` · ``automation`` · ``bot`` · ``chatbot`` · ``css`` · ``docker`` · ``ecommerce`` · ``frontend`` · ``html`` · ``javascript`` · ``llm`` · ``open-source``

> Projeto mantido por [@mkbraion](https://github.com/mkbraion).
<!-- MKBRAION-POLISH:END -->

# AstrBot Brasil 🇧🇷

<p align="center">
  <strong>Agentes de IA, chatbot multicanal e automação em português do Brasil.</strong><br>
  Edição brasileira adaptada e mantida por <a href="https://github.com/mkbraion">@mkbraion</a>.
</p>

<p align="center">
  <img alt="Python 3.12+" src="https://img.shields.io/badge/Python-3.12%2B-blue">
  <img alt="Idioma pt-BR" src="https://img.shields.io/badge/idioma-pt--BR-009c3b">
  <img alt="Licença AGPL-3.0-or-later" src="https://img.shields.io/badge/licen%C3%A7a-AGPL--3.0--or--later-blue">
  <img alt="Edição brasileira" src="https://img.shields.io/badge/edi%C3%A7%C3%A3o-Brasil-ffdf00">
</p>

> **AstrBot Brasil** é uma edição comunitária brasileira baseada no projeto open source AstrBot. O código original não foi criado por @mkbraion; esta edição concentra tradução, localização, documentação, experiência pt-BR e melhorias específicas da distribuição brasileira.

## O que é o AstrBot Brasil?

AstrBot Brasil é uma plataforma de agentes de IA e chatbot que conecta modelos de linguagem a diferentes canais de comunicação. Pode ser usada para assistentes pessoais, automações, atendimento, agentes com ferramentas, bases de conhecimento e experiências de chat com IA.

A edição brasileira prioriza:

- 🇧🇷 interface e documentação em português do Brasil;
- 💻 instalação simples para Windows e PowerShell;
- 🤖 suporte a provedores de IA como OpenAI, Anthropic, Gemini e serviços compatíveis;
- 🧠 Agent, MCP, Skills, personas e base de conhecimento;
- 🌐 dashboard WebUI e ChatUI;
- 🔌 ecossistema de plugins;
- 💬 integração com Telegram, Slack, Discord, LINE e outras plataformas suportadas;
- 🛡️ sandbox e controle de acesso do agente ao computador.

## Captura de tela

A captura anterior mostrava a interface original em inglês e foi removida para não representar incorretamente esta edição. O painel usa português do Brasil por padrão. O catálogo pt-BR cobre todas as chaves da interface e preserva os marcadores de interpolação, com verificação automática no CI. A instalação compila o painel desta edição. Conteúdos de plugins de terceiros, respostas das APIs externas e documentação original em outros idiomas dependem de seus autores.

## Requisitos

- Python 3.12 ou superior;
- Node.js 20 ou superior com npm ou pnpm para compilar o painel;
- Windows 10/11, Linux ou macOS;
- Git para contribuição;
- `uv` recomendado para gerenciamento do ambiente Python.

## Instalação rápida

### Windows — PowerShell

```powershell
python --version
pip install uv
uv tool install astrbot --python 3.12
astrbot init
astrbot run
```

Nas próximas execuções:

```powershell
astrbot run
```

Para atualizar:

```powershell
uv tool upgrade astrbot --python 3.12
```

### Linux

```bash
python3 --version
pip install uv
uv tool install astrbot --python 3.12
astrbot init
astrbot run
```

### macOS

```bash
python3 --version
pip install uv
uv tool install astrbot --python 3.12
astrbot init
astrbot run
```

## Executar pelo código-fonte

No Windows, dentro da pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

Se o PowerShell bloquear `Activate.ps1`:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Docker

```powershell
docker compose up -d
docker compose logs -f
```

Para encerrar:

```powershell
docker compose down
```

## Primeiro acesso

1. Inicie o AstrBot.
2. Abra o endereço informado no terminal.
3. Configure a conta administrativa.
4. Escolha o provedor/modelo de IA.
5. Cadastre sua API key somente no local apropriado da configuração.
6. Configure uma plataforma de mensagens se desejar.
7. Revise as permissões de acesso do Agent ao computador antes de habilitá-las.

> Nunca publique `.env`, tokens, senhas ou API keys no GitHub.

## Recursos principais

- conversas com LLMs e multimodalidade;
- agentes com ferramentas;
- MCP e Skills;
- subagentes;
- compressão automática de contexto;
- personas;
- tarefas agendadas;
- bases de conhecimento;
- plugins e automações;
- dashboard WebUI e ChatUI;
- sistema de internacionalização;
- idioma `pt-BR` como padrão desta edição brasileira.

## Português do Brasil

A edição brasileira registra `pt-BR` diretamente no sistema de internacionalização do dashboard e usa esse idioma como padrão quando não existe preferência salva no navegador.

Termos técnicos consolidados como API, token, plugin, commit, branch, endpoint, prompt, MCP, Docker e Git permanecem em inglês quando isso melhora a clareza ou preserva compatibilidade.

## Solução de problemas

### `python` não é reconhecido

Instale o Python 3.12+ e marque a opção para adicionar o Python ao `PATH`.

### PowerShell bloqueou `Activate.ps1`

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Dashboard aparece em outro idioma

Selecione **Português (Brasil)** no seletor de idioma. Instalações novas desta edição usam `pt-BR` como padrão.

### API de IA não conecta

Confira a API key, a URL do endpoint, o modelo selecionado e as permissões da conta do provedor.

## Perguntas frequentes

**Esta versão é oficial da equipe original do AstrBot?**  
Não. É uma edição comunitária brasileira adaptada e mantida por @mkbraion.

**Posso usar comercialmente?**  
A licença principal é AGPL-3.0-or-later. Uso comercial não é proibido pela AGPL, mas as obrigações da licença continuam valendo.

**Posso remover a licença?**  
Não. Os arquivos e avisos legais aplicáveis devem ser preservados.

## Contribuindo com a edição brasileira

Contribuições são bem-vindas, principalmente para traduções pt-BR, documentação para Windows/PowerShell, acessibilidade, testes de i18n e correção de strings ainda não internacionalizadas.

```powershell
git checkout -b feat/minha-melhoria
git add .
git commit -m "feat(pt-BR): descreva sua melhoria"
git push -u origin feat/minha-melhoria
```

## Roadmap brasileiro

- [x] repositório brasileiro independente;
- [x] README principal em pt-BR;
- [x] identidade da edição brasileira;
- [x] registro do locale `pt-BR` no dashboard;
- [x] idioma brasileiro como padrão da edição;
- [ ] ampliar a cobertura de todas as telas do dashboard;
- [ ] ampliar mensagens de backend e CLI em pt-BR;
- [ ] revisar a documentação técnica completa;
- [ ] adicionar mais testes automatizados de localização.

## Responsável pela edição brasileira

**mkbraion**  
GitHub: https://github.com/mkbraion

Responsável nesta distribuição por localização, tradução, documentação brasileira, manutenção do repositório brasileiro e melhorias específicas desta edição.

## Licença e projeto original

Este repositório contém uma versão modificada baseada no software AstrBot. O projeto principal está licenciado sob **GNU Affero General Public License v3 ou posterior (AGPL-3.0-or-later)**. O arquivo `LICENSE` deve permanecer no repositório e os avisos legais aplicáveis devem ser preservados.

A AGPL exige, entre outras condições, que versões modificadas distribuídas permaneçam sob os termos aplicáveis da licença e contempla obrigações de disponibilização do código-fonte correspondente quando o software modificado é usado para interação por rede.

O dashboard também contém componentes de terceiros licenciados separadamente. O arquivo `dashboard/LICENSE` preserva a licença MIT e o respectivo aviso de copyright aplicável.

Arquivos como `EULA.md`, `FIRST_NOTICE*.md`, cabeçalhos de copyright e demais avisos legais existentes devem ser preservados quando exigido pelos termos aplicáveis.

**AstrBot Brasil não é apresentado como uma distribuição oficial administrada pelos mantenedores do projeto original.** A edição brasileira é adaptada e mantida por **@mkbraion**.
