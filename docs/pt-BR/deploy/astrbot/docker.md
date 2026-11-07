# Implantar o AstrBot com Docker

> [!WARNING]
> O Docker oferece uma maneira prática de implantar o AstrBot no Windows, macOS e Linux.
>
> Este tutorial pressupõe que o Docker já esteja instalado no seu ambiente. Caso ainda não esteja, consulte a [documentação oficial do Docker](https://docs.docker.com/get-docker/) para obter as instruções de instalação.

## Implantar com Docker Compose

::: details Implantar somente o AstrBot (método geral)

Primeiro, clone o repositório do AstrBot para o seu computador:

```bash
git clone https://github.com/AstrBotDevs/AstrBot
cd AstrBot
```

Em seguida, execute o Compose:

```bash
sudo docker compose up -d
```

> [!TIP]
> Se sua rede estiver na China continental, o comando acima poderá não conseguir baixar a imagem. Nesse caso, talvez seja necessário editar o arquivo `compose.yml` e substituir `image: soulter/astrbot:latest` por `image: m.daocloud.io/docker.io/soulter/astrbot:latest`.
:::

::: details Implantar com o ambiente Agent Sandbox

Oferece suporte à execução nativa de código Python, à execução de comandos Shell e a outros recursos.

Procedimento de implantação:

```bash
git clone https://github.com/AstrBotDevs/AstrBot
cd AstrBot
# Modifique a configuração das variáveis de ambiente no arquivo compose-with-shipyard.yml, como o token de acesso do Shipyard.
docker compose -f compose-with-shipyard.yml up -d
docker pull soulter/shipyard-ship:latest
```

Para consultar os detalhes de configuração e uso, leia a documentação do [ambiente Agent Sandbox](/en/use/astrbot-agent-sandbox.md).
:::

## Implantar com Docker

```bash
mkdir astrbot
cd astrbot
sudo docker run -itd -p 6185:6185 -p 6199:6199 -v $PWD/data:/AstrBot/data -v /etc/localtime:/etc/localtime:ro -v /etc/timezone:/etc/timezone:ro --name astrbot soulter/astrbot:latest
```

> [!TIP]
> Se sua rede estiver na China continental, o comando acima poderá não conseguir baixar a imagem. Use o comando abaixo para baixá-la:
>
> ```bash
> sudo docker run -itd -p 6185:6185 -p 6199:6199 -v $PWD/data:/AstrBot/data -v /etc/localtime:/etc/localtime:ro -v /etc/timezone:/etc/timezone:ro --name astrbot m.daocloud.io/docker.io/soulter/astrbot:latest
> ```
>
> (Agradecimentos à DaoCloud ❤️)

> No Windows, não é necessário adicionar `sudo`; o mesmo vale para os comandos abaixo.
> Sincronizar o horário do host no Windows (requer WSL2):

```
-v \\wsl.localhost\(your-wsl-os)\etc\timezone:/etc/timezone:ro
-v \\wsl.localhost\(your-wsl-os)\etc\localtime:/etc/localtime:ro
```

Para acompanhar os logs do AstrBot, execute:

```bash
sudo docker logs -f astrbot
```

## Implantar pelo Docker Desktop no Windows

### No Prompt de Comando (CMD) do Windows

Defina `TZ` usando o formato padrão de fuso horário IANA (`Região/Cidade`). Para a China, use `Asia/Shanghai`.

```bash
docker run -itd -p 6185:6185 -p 6199:6199 -e TZ=Asia/Shanghai -v "%cd%\data:/AstrBot/data" --name astrbot soulter/astrbot:latest
```

> [!TIP]
> Se sua rede estiver na China continental, o comando acima poderá não conseguir baixar a imagem. Use o comando abaixo para baixá-la:
>
> ```bash
> docker run -itd -p 6185:6185 -p 6199:6199 -e TZ=Asia/Shanghai -v "%cd%\data:/AstrBot/data" --name astrbot m.daocloud.io/docker.io/soulter/astrbot:latest
> ```
>
> (Agradecimentos à DaoCloud ❤️)

### No PowerShell

Defina `TZ` usando o formato padrão de fuso horário IANA (`Região/Cidade`). Para a China, use `Asia/Shanghai`.

```powershell
docker run -itd -p 6185:6185 -p 6199:6199 -e TZ=Asia/Shanghai -v "${PWD}\data:/AstrBot/data" --name astrbot soulter/astrbot:latest
```

> [!TIP]
> Se sua rede estiver na China continental, o comando acima poderá não conseguir baixar a imagem. Use o comando abaixo para baixá-la:
>
> ```powershell
> docker run -itd -p 6185:6185 -p 6199:6199 -e TZ=Asia/Shanghai -v "${PWD}\data:/AstrBot/data" --name astrbot m.daocloud.io/docker.io/soulter/astrbot:latest
> ```
>
> (Agradecimentos à DaoCloud ❤️)

## 🎉 Tudo pronto!

Se tudo correr bem, você verá os logs do AstrBot.

Se não houver erros, será exibida uma mensagem de log semelhante a `🌈 Dashboard started, accessible at`, acompanhada de vários links. Abra um deles para acessar o painel do AstrBot.

> [!TIP]
> Como o Docker isola o ambiente de rede, você não poderá usar `localhost` para acessar o painel.
>
> Novos usuários devem usar a senha aleatória exibida nos logs de inicialização para entrar pela primeira vez. Use o nome de usuário mostrado nos logs (geralmente `astrbot`) e altere a senha após o primeiro acesso.
>
> Se a implantação for feita em um servidor na nuvem, abra as portas `6180-6200` e `11451` no painel do provedor de nuvem.

Em seguida, implante uma plataforma de mensagens para usar o AstrBot nela.

## Redefinir a senha do painel

Se você esquecer a senha do painel, poderá redefini-la usando a CLI integrada do AstrBot dentro do contêiner:

```bash
sudo docker exec -it astrbot astrbot password
```

O primeiro `astrbot` é o nome do contêiner; substitua-o pelo nome real do seu contêiner (consulte a saída de `sudo docker ps`).

Siga as instruções para informar uma nova senha. Para alterar também o nome de usuário:

```bash
sudo docker exec -it astrbot astrbot password --username <new-username>
```

> [!TIP]
> A nova senha entrará em vigor depois que o contêiner for reiniciado: `sudo docker restart astrbot`.

## Configurar um proxy HTTP no Docker

Configure o proxy HTTP na WebUI, em `Settings → Network → Proxy & Dependency Sources → HTTP Proxy`. O AstrBot acessa esse endereço **de dentro do próprio contêiner**. Portanto, `http://127.0.0.1:7890` aponta para o contêiner do AstrBot, e não para o host nem para outro contêiner.

Se o proxy estiver em execução no host ou em outro contêiner cuja porta esteja publicada no host:

- macOS / Windows (Docker Desktop): `http://host.docker.internal:7890`
- Linux: `http://172.17.0.1:7890` (substitua `172.17.0.1` pelo gateway da interface `docker0`, caso seja diferente)

Se o AstrBot e o proxy compartilharem uma rede Docker, use o nome do contêiner do proxy, por exemplo, `http://clash:7890`.

Clientes baseados no Clash geralmente usam HTTP na porta `7890` e SOCKS na porta `7891`. Use `http://` ou `socks5://` de acordo com o protocolo. Se o proxy estiver instalado no host, ele deverá escutar em uma interface do host acessível pelo Docker, como `0.0.0.0` ou a interface do gateway do Docker, e não somente em `127.0.0.1`. Publique a porta do proxy no host.
