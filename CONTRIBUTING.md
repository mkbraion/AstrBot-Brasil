# Contribuindo com o AstrBot Brasil 🇧🇷

Obrigado pelo interesse em melhorar a edição brasileira.

## Antes de começar

Esta distribuição é uma versão modificada do AstrBot e permanece sujeita às licenças e avisos legais aplicáveis. Não remova `LICENSE`, `dashboard/LICENSE`, avisos de copyright ou outros documentos cuja preservação seja necessária.

## Como contribuir

1. Crie uma branch para sua alteração.
2. Faça alterações pequenas e objetivas.
3. Preserve nomes de APIs, classes, funções, variáveis de ambiente e protocolos quando a tradução puder quebrar compatibilidade.
4. Para textos de interface, use português brasileiro natural.
5. Execute os testes relacionados.
6. Abra um pull request descrevendo o que foi alterado.

### Exemplo no PowerShell

```powershell
git checkout -b feat/minha-melhoria
git add .
git status
git commit -m "feat(pt-BR): descreva sua melhoria"
git push -u origin feat/minha-melhoria
```

## Padrão de português

Use `pt-BR`, com vocabulário natural do Brasil. Termos técnicos amplamente usados, como API, token, plugin, commit, branch, endpoint, prompt, framework, CLI, SDK, Docker, Git e GitHub podem permanecer em inglês.

## Localização do dashboard

Os arquivos de tradução ficam em:

```text
dashboard/src/i18n/locales/pt-BR/
```

Ao adicionar uma chave visível ao usuário, atualize o pacote `pt-BR` correspondente.

## Backend, CLI e plugins

Textos exibidos ao usuário também existem em arquivos Python e nos pacotes i18n de plugins internos. Não traduza identificadores usados pelo código.

## Testes recomendados

### Python

```powershell
python -m pytest
python -m ruff check astrbot
```

### Dashboard

```powershell
cd dashboard
pnpm install
pnpm build
```

## Segurança

Nunca envie:

- `.env`;
- API keys;
- tokens;
- senhas;
- cookies;
- credenciais;
- bancos de dados locais;
- conteúdo privado de usuários.

Revise `git status` e `git diff --cached` antes do push.

## Responsável pela edição brasileira

A edição brasileira é desenvolvida e mantida por **mkbraion**.

GitHub: https://github.com/mkbraion

Contribuir com esta edição não altera a autoria do código preexistente proveniente do projeto-base.
