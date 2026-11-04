# CLI do AstrBot {#cli-commands}

A CLI do AstrBot inicializa instâncias, inicia o AstrBot, atualiza configurações comuns e gerencia plugins.

Se você instalar o AstrBot com `uv`:

```bash
uv tool install astrbot --python 3.12
```

O `uv` cria o executável `astrbot` e o adiciona ao `PATH`. Para conferir onde ele está instalado, use:

::: code-group

```bash [Linux / macOS]
which astrbot
```

```powershell [Windows]
where.exe astrbot
```

:::

> [!TIP]
> Execute os comandos abaixo a partir do diretório de trabalho do AstrBot.

## Início rápido

Inicialize o diretório uma única vez e, em seguida, inicie o AstrBot:

```bash
astrbot init
astrbot run
```

O comando `astrbot init` cria os diretórios de dados e os arquivos de configuração necessários para o AstrBot. Depois da inicialização, use `astrbot run` nas próximas vezes em que iniciar o programa.

## Comandos principais

| Comando | Finalidade |
| --- | --- |
| `astrbot init` | Inicializa o diretório atual como diretório de trabalho do AstrBot. |
| `astrbot run` | Inicia o AstrBot em primeiro plano. |
| `astrbot conf` | Consulta ou atualiza valores comuns de configuração. |
| `astrbot password` | Altera interativamente a senha de acesso à WebUI. |
| `astrbot plug` | Cria, instala, atualiza, remove ou pesquisa plugins. |
| `astrbot help` | Exibe a ajuda da CLI. |
| `astrbot --version` | Exibe a versão da CLI do AstrBot. |

## Inicialização

O comando `astrbot init` prepara o diretório de trabalho do AstrBot e solicita confirmação antes de criar os arquivos e diretórios necessários. Em instalações automatizadas, você pode pular essa confirmação com `-y` ou `--yes`:

| Opção | Finalidade |
| --- | --- |
| `-y, --yes` | Pula as perguntas de confirmação durante a inicialização. |

Exemplos:

```bash
astrbot init --yes
astrbot init -y
```

## Iniciar o AstrBot

```bash
astrbot run
```

Opções mais utilizadas:

| Opção | Finalidade |
| --- | --- |
| `-p, --port <PORT>` | Define a porta da WebUI. |
| `-r, --reload` | Ativa a recarga automática de plugins durante o desenvolvimento. |
| `--reset-password` | Redefine a senha inicial da WebUI na inicialização e exibe a nova senha nos logs de inicialização. |

Exemplos:

```bash
astrbot run --port 6185
astrbot run --reload
astrbot run --reset-password
```

Se você esquecer a senha de acesso à WebUI, execute este comando a partir do diretório de trabalho do AstrBot:

```bash
astrbot run --reset-password
```

O AstrBot gera uma nova senha inicial durante a inicialização e a exibe nos logs. Depois de entrar na WebUI, altere a senha imediatamente.

Ao iniciar diretamente a partir do código-fonte, você também pode executar:

```bash
python main.py --reset-password
```

## Configuração

O comando `astrbot conf` consulta e atualiza valores comuns de configuração.

```bash
astrbot conf get
astrbot conf get dashboard.port
astrbot conf set dashboard.port 6185
```

Chaves compatíveis:

| Chave | Descrição |
| --- | --- |
| `timezone` | Fuso horário, por exemplo `America/Sao_Paulo`. |
| `log_level` | Nível de log: `DEBUG`, `INFO`, `WARNING`, `ERROR` ou `CRITICAL`. |
| `dashboard.port` | Porta da WebUI. |
| `dashboard.username` | Nome de usuário da WebUI. |
| `dashboard.password` | Senha da WebUI. |
| `callback_api_base` | URL base da API de callback. Deve começar com `http://` ou `https://`. |

Ao alterar a senha do dashboard, os hashes da senha atual são atualizados automaticamente:

```bash
astrbot conf set dashboard.password "new-password"
```

Você também pode usar o comando interativo específico para senha:

```bash
astrbot password
astrbot password --username admin
```

## Plugins

O comando `astrbot plug` gerencia os plugins localizados em `data/plugins`.

| Comando | Finalidade |
| --- | --- |
| `astrbot plug list` | Lista os plugins instalados. |
| `astrbot plug list --all` | Também exibe os plugins não instalados. |
| `astrbot plug search <QUERY>` | Pesquisa plugins. |
| `astrbot plug install <NAME>` | Instala um plugin. |
| `astrbot plug update [NAME]` | Atualiza um plugin específico ou todos os que podem ser atualizados, caso nenhum nome seja informado. |
| `astrbot plug remove <NAME>` | Remove um plugin instalado. |
| `astrbot plug new <NAME>` | Cria um novo plugin a partir do modelo. |

Use um proxy do GitHub ao instalar ou atualizar plugins:

```bash
astrbot plug install example-plugin --proxy https://gh-proxy.example.com/
astrbot plug update --proxy https://gh-proxy.example.com/
```

Para criar um plugin, informe o autor, a descrição, a versão e a URL do repositório quando solicitado:

```bash
astrbot plug new my-plugin
```

## Ajuda

Exiba a ajuda geral da CLI:

```bash
astrbot help
```

Exiba a ajuda de um comando específico:

```bash
astrbot help run
astrbot run --help
astrbot help conf
astrbot plug --help
```

Exiba a versão:

```bash
astrbot --version
```
