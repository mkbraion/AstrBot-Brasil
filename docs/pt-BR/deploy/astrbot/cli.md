# Implantar o AstrBot a partir do código-fonte

> [!WARNING]
> Você está implantando este projeto diretamente a partir do código-fonte. Este tutorial exige conhecimentos técnicos básicos.
>
> Este tutorial pressupõe que o Python já esteja instalado no dispositivo, na versão `>=3.12`.

## Baixar/clonar o repositório

Se o `git` estiver instalado no computador, você poderá baixar o código-fonte com o seguinte comando:

```bash
git clone https://github.com/AstrBotDevs/AstrBot.git
# O comando acima baixa o commit mais recente do código-fonte. Para baixar a versão estável mais recente, use o comando abaixo:
# git clone --depth=1 --branch $(git ls-remote --tags --sort='-v:refname' https://github.com/AstrBotDevs/AstrBot.git | head -n1 | awk -F/ '{print $3}') https://github.com/AstrBotDevs/AstrBot.git
cd AstrBot
```

Se o `git` não estiver instalado, baixe-o e instale-o primeiro.

Como alternativa, baixe o código-fonte diretamente do GitHub e extraia o arquivo:

![Imagem ilustrativa do download do código-fonte](https://files.astrbot.app/docs/source/images/cli/image.png)

## Instalar dependências e executar

::: details 【🥳Recomendado】Use `uv` para gerenciar as dependências

> Se o `uv` não estiver instalado, consulte [Instalação do uv](https://docs.astral.sh/uv/getting-started/installation/).

No terminal, dentro do diretório do AstrBot, execute:

```bash
uv sync
uv run main.py
```

Se você tiver instalado plugins, recomendamos adicionar o parâmetro `--no-sync` nas próximas inicializações para evitar que as dependências dos plugins sejam instaladas novamente. Estamos trabalhando para resolver esse problema. Fique atento às novidades.

```bash
uv run --no-sync main.py
```
:::

::: details Instalar dependências com o `venv` integrado ao Python

No diretório do código-fonte do AstrBot, execute o seguinte comando no terminal:

> No Windows, se você baixou e extraiu o código-fonte diretamente, abra a pasta extraída e digite o comando na barra de endereço:
> ![Imagem ilustrativa da barra de endereço do Explorador de Arquivos](https://files.astrbot.app/docs/source/images/cli/image-1.png)

```bash
python3 -m venv ./venv
```

> O comando pode ser `python` em vez de `python3`.

As etapas acima criarão e ativarão um ambiente virtual (para evitar interferências no ambiente Python local).

Em seguida, instale as dependências com o comando abaixo. Esse processo pode levar algum tempo.

Execute no macOS/Linux/WSL:

```bash
source venv/bin/activate
python -m pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
python main.py
```

Execute no Windows:

```bash
venv\Scripts\activate
python -m pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
python main.py
```
:::

## 🎉 Tudo pronto!

Se tudo correr bem, você verá os logs do AstrBot no terminal.

Se não houver erros, será exibida uma mensagem de log semelhante a `🌈 Dashboard started, accessible at`, acompanhada de vários links. Abra um deles para acessar o painel do AstrBot. O endereço é `http://localhost:6185`.

> [!TIP]
> Se você estiver implantando o AstrBot em um servidor, substitua `localhost` pelo endereço IP do servidor.
>
> Novos usuários devem usar a senha aleatória exibida nos logs de inicialização para entrar pela primeira vez. Use o nome de usuário mostrado nos logs (geralmente `astrbot`) e altere a senha após o primeiro acesso.

Em seguida, implante uma plataforma de mensagens para usar o AstrBot nela.
