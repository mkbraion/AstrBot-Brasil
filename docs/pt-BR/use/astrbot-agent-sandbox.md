# Ambiente Agent Sandbox

## O que é?

A IA integrada do AstrBot permite que o Agent acesse um ambiente computacional executando código, lendo e gravando arquivos e realizando outras operações. No AstrBot, esse recurso é chamado de **Agent Computer Use** (uso do computador pelo Agent).

Atualmente, o Agent Computer Use oferece suporte a dois ambientes de execução:

- **Ambiente local**: o Agent do AstrBot executa código e operações com arquivos **diretamente no ambiente em que o AstrBot está sendo executado**, acessando seus arquivos e comandos. Com o uso do `Seatbelt` no macOS ou do `bubblewrap (bwrap)` no Linux, o AstrBot pode oferecer **acesso restrito a arquivos e execução de código**, limitando o escopo de acesso aos arquivos e as permissões de rede de diferentes usuários do bot para aumentar a segurança do ambiente local.
- **Ambiente de sandbox de terceiros**: o Agent do AstrBot executa código e operações com arquivos em um **ambiente separado**, sem acesso direto aos arquivos e comandos do host ou de dentro do contêiner do AstrBot. Essa separação pode oferecer um isolamento mais forte; o acesso a arquivos, a rede e o isolamento entre usuários dependem dos recursos e da configuração da sandbox. Em geral, sandboxes de terceiros exigem implantação e configuração adicionais, além de mais recursos computacionais.

Abra **Configuração → IA → Recursos → Agent Computer Use** (na interface em inglês: **Config → AI → Capabilities → Agent Computer Use**) e defina **Ambiente de execução do Computer Use** (`Computer Use Runtime`) como **Máquina local** (`Local machine`) ou **Sandbox de terceiros** (`Third-party sandbox`).

Na opção Máquina local, o AstrBot tenta habilitar o isolamento no ambiente de execução. A disponibilidade depende do sistema operacional, do kernel, das permissões da conta e das políticas de segurança do sistema. Consulte a seção [Ambiente local](#local-environment) abaixo.

Na opção Sandbox de terceiros, selecione também um **Driver de sandbox** (`Sandbox Driver`) e configure o endpoint, o token de acesso e as demais opções. Consulte a seção [Ambiente de sandbox de terceiros](#third-party-sandbox-environment) abaixo.

## Ambiente local {#local-environment}

Abra **Configuração → IA → Recursos → Agent Computer Use** e defina **Ambiente de execução do Computer Use** (`Computer Use Runtime`) como **Máquina local** (`local`).

O AstrBot fornece ao Agent um conjunto de ferramentas, incluindo Shell, Python e ferramentas de sistema de arquivos, para acessar o ambiente local.

> [!NOTE]
> Se o AstrBot estiver sendo executado no Docker, o ambiente local será o ambiente Linux dentro do contêiner do AstrBot, e não o host do Docker. O acesso a arquivos e à rede continua sujeito à configuração do contêiner.

As permissões de membros e administradores são configuradas separadamente, conforme a matriz abaixo.

![Matriz de políticas de permissão local](/en/use/images/config-local-permissions-en.png)

Ao habilitar **Executar código** (`Execute code`), o Agent recebe as ferramentas `astrbot_execute_shell` e `astrbot_execute_python` para executar comandos Shell e código Python no ambiente local.

Ao habilitar **Permitir rede durante a execução** (`Allow network during execution`), o acesso à rede durante a execução de Shell/Python é permitido. Caso contrário, o acesso à rede durante a execução fica restrito.

> [!TIP]
> Essa configuração de rede controla se Shell/Python pode acessar a rede por meio de comandos como `curl` ou `wget`. Ela não controla o recurso [Pesquisa na Web](/en/use/websearch).

O **Escopo de acesso a arquivos** (`File access scope`) tem três opções: **Desativado** (`Disabled`), **Espaço de trabalho** (`Workspace`) e **Ambiente inteiro** (`Entire environment`):

- **Desativado**: o Agent não pode acessar arquivos pelas ferramentas locais de Computer Use; as ferramentas de sistema de arquivos ficam indisponíveis.
- **Espaço de trabalho**: as ferramentas de sistema de arquivos ficam limitadas ao espaço de trabalho da sessão do usuário atual (identificado por UMO) e aos diretórios abaixo:
  - Diretório do espaço de trabalho, em `data/workspaces/<normalized_umo>/`: **leitura e gravação**. Projetos do ChatUI também podem usar um espaço de trabalho compartilhado do projeto ou um espaço de trabalho personalizado.
  - Diretório temporário do AstrBot, `data/temp/`: **leitura e gravação**.
  - Diretório temporário das ferramentas, `<system temporary directory>/.astrbot/`: **leitura e gravação**.
  - Skills do Agent instaladas, `data/skills/`: **somente leitura para membros; leitura e gravação para administradores**.
  - Skills fornecidas por plugins, `data/plugins/<plugin_name>/skills/`: **somente leitura**.
  - Skills de plugins integrados, `<AstrBot source or installation directory>/astrbot/builtin_stars/<plugin_name>/skills/`: **somente leitura**.
- **Ambiente inteiro**: o Agent pode acessar arquivos em todo o ambiente local, respeitando as permissões da conta que executa o AstrBot.

O AstrBot fornece `astrbot_file_read_tool`, `astrbot_file_write_tool`, `astrbot_file_edit_tool` e `astrbot_grep_tool` para leitura, gravação, edição e pesquisa de conteúdo em arquivos, respectivamente. Quando a execução restrita de código está habilitada, o backend de isolamento também disponibiliza as ferramentas do sistema, as bibliotecas e o ambiente Python necessários para executar código.

A matriz de permissões aplica as seguintes dependências:

- Quando **Executar código** estiver desmarcado, **Permitir rede durante a execução** não poderá ser marcado, pois **as permissões de rede só se aplicam durante a execução de código**.
- Quando o **Escopo de acesso a arquivos** estiver definido como **Desativado**, não será possível habilitar a execução nem o acesso à rede, pois **a execução de código e o acesso à rede dependem do acesso a arquivos**.

Se o seu ambiente **não atender aos requisitos para o isolamento local**, por exemplo, Windows sem um backend de isolamento compatível, Linux sem bubblewrap ou macOS sem um iniciador Seatbelt utilizável, a opção de rede ficará oculta. As seguintes combinações de permissões continuarão disponíveis:

- Escopo de acesso a arquivos: Desativado; Executar código: Não.
- Escopo de acesso a arquivos: Espaço de trabalho; Executar código: Não. Essa opção está disponível no Linux/macOS; o acesso restrito aos arquivos do espaço de trabalho ainda não é compatível com o Windows nativo.
- Escopo de acesso a arquivos: Ambiente inteiro; Executar código: Não.
- Escopo de acesso a arquivos: Ambiente inteiro; Executar código: Sim. Não será possível restringir separadamente o acesso à rede durante a execução.

Se o isolamento local não estiver disponível, siga as instruções correspondentes ao seu sistema operacional e ao ambiente de implantação abaixo.

### Usuários de macOS {#local-macos}

O Seatbelt é o mecanismo de sandbox integrado ao macOS. O AstrBot usa `/usr/bin/sandbox-exec` para iniciar o Seatbelt e restringir o escopo de acesso do Agent a arquivos e as permissões de rede. Normalmente, o macOS já inclui `/usr/bin/sandbox-exec`.

1. No Mac que executa o AstrBot, verifique se a ferramenta do sistema existe:

   ```bash
   ls -l /usr/bin/sandbox-exec
   ```

2. Verifique se o sistema permite executá-la:

   ```bash
   /usr/bin/sandbox-exec -p '(version 1) (allow default)' /usr/bin/true
   ```

   O código de saída `0` significa que essa verificação simples foi aprovada. O AstrBot também verifica as restrições reais do espaço de trabalho durante a inicialização.

Se o sistema não fornecer a ferramenta ou se as políticas impedirem seu uso, mude para um [ambiente de sandbox de terceiros](#third-party-sandbox-environment).

Se o AstrBot estiver sendo executado no Docker em um Mac, siga as instruções para [usuários de Docker](#local-docker) abaixo. O Seatbelt do host não é usado diretamente pelos processos dentro de um contêiner Linux.

### Usuários de Linux {#local-linux}

O [bubblewrap](https://github.com/containers/bubblewrap) é uma ferramenta de sandbox em espaço de usuário para Linux.

Verifique se o bubblewrap está instalado e consegue iniciar:

```bash
command -v bwrap
bwrap --unshare-all --ro-bind / / --proc /proc --dev /dev /bin/sh -c 'echo "AstrBot is good to go!"'
```

Se o comando exibir `AstrBot is good to go!`, o bubblewrap está instalado e passou nessa verificação básica de inicialização.

Se o bubblewrap não estiver instalado, use o gerenciador de pacotes da sua distribuição:

::: code-group

```bash [Debian / Ubuntu]
sudo apt update
sudo apt install bubblewrap
```

```bash [Fedora]
sudo dnf install bubblewrap
```

```bash [Arch Linux]
sudo pacman -S bubblewrap
```

:::

Se a inicialização falhar:

- **`bwrap` não encontrado**: verifique se ele está instalado no ambiente que executa o AstrBot e se está no `PATH` usado durante a inicialização do processo.
- **`Operation not permitted` ou erros de namespace de usuário**: verifique os limites de namespaces de usuário, o AppArmor e outras políticas de segurança do sistema. Use `sysctl user.max_user_namespaces` para consultar o limite de namespaces e `sudo journalctl -k` para consultar os logs relevantes do kernel.
- **Bloqueio pelo AppArmor**: siga as instruções da sua distribuição para permitir a criação de namespaces de usuário pelo ambiente de execução real. Não desative as políticas de segurança de toda a máquina apenas para passar nessa verificação.
- **Implantação em contêiner**: siga as instruções para [usuários de Docker](#local-docker). Instalar o `bwrap` no host não o instala dentro do contêiner.

Reinicie o AstrBot depois de corrigir o ambiente. A verificação de inicialização determinará se a execução no Espaço de trabalho e o controle de rede estão disponíveis. Se **Permitir rede durante a execução** aparecer na matriz de permissões, o isolamento local foi habilitado com sucesso.

### Usuários de Docker {#local-docker}

A imagem Docker do AstrBot é executada como um contêiner Linux.

O Docker já oferece isolamento no nível do contêiner. Por padrão, o AstrBot pode acessar os arquivos dentro do contêiner e os volumes montados, e não todo o sistema de arquivos do host. O acesso à rede também está sujeito à configuração de rede do Docker. O isolamento local usa o bubblewrap dentro do contêiner para restringir ainda mais **o acesso aos arquivos do espaço de trabalho e à rede durante a execução**. Se você precisa apenas acessar os arquivos do contêiner e os volumes montados, pode continuar usando Ambiente inteiro; o bwrap não é obrigatório em toda implantação do Computer Use.

Instalar o bwrap é apenas uma parte da configuração. Habilitar o isolamento local dentro do Docker é **relativamente complexo**, e **as implantações Docker padrão talvez não permitam sua inicialização**, pois as configurações de namespaces de usuário do host, seccomp, AppArmor e as permissões do contêiner também se aplicam. Para execução isolada, considere um [ambiente de sandbox de terceiros](#third-party-sandbox-environment). Se ainda precisar do isolamento local dentro do contêiner, consulte as orientações da plataforma de contêineres utilizada e configure políticas como seccomp para permitir os namespaces de usuário exigidos pelo bwrap.

### Usuários de Windows {#local-windows}

Atualmente, o isolamento local não é compatível com o Windows nativo. Em vez disso, você pode usar um [ambiente de sandbox de terceiros](#third-party-sandbox-environment).

## Ambiente de sandbox de terceiros {#third-party-sandbox-environment}

As sandboxes de terceiros são um recurso opcional do AstrBot. Elas permitem que o Agent execute código e operações com arquivos em um **ambiente separado**, sem acesso direto aos arquivos e comandos do host ou de dentro do contêiner do AstrBot. Os drivers de sandbox compatíveis incluem:

- **Shipyard Neo**: o driver atualmente recomendado. É composto por Bay, Ship e Gull, que fornecem, respectivamente, a API do plano de controle, recursos de Python/Shell/sistema de arquivos e automação de navegador.
- **CUA**: um ambiente de execução de sandbox para Computer Use que pode criar sandboxes Linux, macOS, Windows, Android e outros tipos, além de disponibilizar interfaces de Shell, captura de tela, mouse, teclado e sistema de arquivos.
- **Shipyard**: o driver legado, mantido por compatibilidade com implantações existentes. O Bay fornece a API do plano de controle, e o Ship fornece recursos de Python/Shell/sistema de arquivos.

> [!TIP]
> Os recursos de sandbox de terceiros ainda estão em prévia técnica. Relate problemas no [GitHub](https://github.com/AstrBotDevs/AstrBot/issues).

<span id="configuring-astrbot-to-use-the-sandbox-environment"></span>

### Habilitar o ambiente de sandbox {#enabling-the-sandbox-environment}

1. Abra **Configuração → IA → Recursos → Agent Computer Use** e defina **Ambiente de execução do Computer Use** (`Computer Use Runtime`) como **Sandbox de terceiros** (`sandbox`).
2. Escolha **Shipyard Neo**, **Shipyard** ou **CUA** como driver de sandbox.
3. **Implante o serviço usando as instruções correspondentes abaixo** e, em seguida, configure o endpoint, o token ou as opções de imagem.
4. Clique em **Salvar** no canto inferior direito da página e teste se o ambiente está funcionando.

### Requisitos de desempenho {#performance-requirements}

Os limites de recursos dependem do driver e do perfil; não existe um único limite de CPU ou memória compartilhado por todos os drivers. Recomenda-se um host com pelo menos **4 CPUs e 8 GB de memória**. O uso real de recursos depende bastante da quantidade de usuários do bot, da frequência com que eles utilizam o recurso e das cargas de trabalho executadas.

<span id="recommended-use-shipyard-neo"></span>

### Shipyard Neo {#shipyard-neo}

O `Shipyard Neo` agora é o driver padrão. Ele é composto por Bay, Ship e Gull:

- **Bay**: a API do plano de controle responsável por criar e gerenciar sandboxes.
- **Ship**: fornece recursos de Python / Shell / sistema de arquivos.
- **Gull**: fornece recursos de automação de navegador.

No `Shipyard Neo`, a raiz do espaço de trabalho é fixa em `/workspace`. Ao usar as ferramentas de sistema de arquivos no AstrBot, informe **caminhos relativos à raiz do espaço de trabalho**, por exemplo, `reports/result.txt`, e não `/workspace/reports/result.txt`.

> [!TIP]
> O recurso de navegador não está disponível em todos os perfis do `Shipyard Neo`. O AstrBot só disponibiliza as ferramentas relacionadas ao navegador quando o perfil selecionado oferece o recurso `browser`. Um exemplo típico é `browser-python`.

#### Implantar o Shipyard Neo separadamente

Se você pretende usar o `Shipyard Neo` por um longo período, geralmente é melhor **implantá-lo separadamente em uma máquina com mais recursos**, como seu homelab, um servidor na rede local ou um host dedicado na nuvem, e então permitir que o AstrBot se conecte remotamente ao Bay.

Isso ocorre porque o `Shipyard Neo` pode consumir muitos recursos quando o recurso de navegador está habilitado, pois precisa executar um ambiente completo de navegador. **Em servidores de nuvem com recursos limitados**, implantar o AstrBot e o `Shipyard Neo` na mesma máquina normalmente exerce uma pressão significativa sobre a CPU e a memória, o que pode prejudicar a estabilidade e a experiência geral.

Um fluxo básico de implantação é:

```bash
git clone https://github.com/AstrBotDevs/shipyard-neo
cd shipyard-neo/deploy/docker
# Altere as principais configurações em config.yaml, como security.api_key
docker compose up -d
```

Após a implantação:

- Por padrão, o Bay escuta em `http://<your-host>:8114`.
- No console do AstrBot, escolha o driver `Shipyard Neo`.
- Defina `Shipyard Neo API Endpoint` como o endereço correspondente, por exemplo, `http://<your-host>:8114`.
- Defina `Shipyard Neo Access Token` como a chave de API do Bay; se o AstrBot puder acessar o arquivo `credentials.json` do Bay, você também poderá deixar o campo vazio e permitir que o AstrBot descubra a credencial automaticamente.

#### Referência: exemplo completo de `config.yaml` (com observações)

Se quiser personalizar os parâmetros de implantação do `Shipyard Neo`, consulte o exemplo completo abaixo, adaptado de [`deploy/docker/config.yaml`](https://github.com/AstrBotDevs/shipyard-neo/blob/main/deploy/docker/config.yaml). Ele mantém a estrutura padrão e adiciona observações explicativas para facilitar o entendimento de cada opção.

> [!TIP]
> A única alteração obrigatória é `security.api_key`. Se não souber para que servem as outras opções, geralmente é melhor manter os valores padrão inicialmente e ajustar apenas os perfis, os limites de recursos e as configurações do pool aquecido conforme necessário.

```yaml
# Configuração de produção do Bay - Docker Compose (modo container_network)
#
# O Bay é executado dentro do Docker e se comunica com os contêineres Ship/Gull
# por meio de uma rede Docker compartilhada.
# Nesse modo, os contêineres de sandbox não precisam publicar portas no host.
#
# No mínimo, atualize:
#   1. security.api_key — defina um segredo aleatório forte

server:
  # Endereço em que a API do Bay escuta
  host: "0.0.0.0"
  # Porta em que a API do Bay escuta
  port: 8114

database:
  # SQLite é o padrão para implantações de nó único.
  # Para implantações com várias instâncias / alta disponibilidade, você pode usar PostgreSQL, por exemplo:
  # url: "postgresql+asyncpg://user:pass@db-host:5432/bay"
  url: "sqlite+aiosqlite:///./data/bay.db"
  echo: false

driver:
  # Docker é o driver padrão
  type: docker

  # Define se as imagens serão baixadas ao criar novas sandboxes.
  # Em produção, geralmente recomenda-se always para obter as imagens mais recentes.
  image_pull_policy: always

  docker:
    # Endpoint do socket do Docker
    socket: "unix:///var/run/docker.sock"

    # Quando Bay, Ship e Gull são executados em contêineres,
    # container_network é recomendado para comunicação direta pela rede dos contêineres.
    connect_mode: container_network

    # Nome da rede compartilhada; deve corresponder à rede em docker-compose.yaml
    network: "bay-network"

    # Define se as portas dos contêineres de sandbox serão publicadas no host.
    # Em geral, recomenda-se desabilitar essa opção em produção.
    publish_ports: false
    host_port: null

cargo:
  # Caminho raiz de armazenamento do Cargo no lado do Bay
  root_path: "/var/lib/bay/cargos"
  # Limite padrão de tamanho do espaço de trabalho (MB)
  default_size_limit_mb: 1024
  # Caminho montado dentro da sandbox. Esta é a raiz do espaço de trabalho do AstrBot/Neo.
  mount_path: "/workspace"

security:
  # Obrigatório: defina um segredo aleatório forte, por exemplo: openssl rand -hex 32
  api_key: "CHANGE-ME"
  # Define se o acesso anônimo é permitido. false é recomendado para produção.
  allow_anonymous: false

# Injeção de variáveis de ambiente de proxy nos contêineres.
# Quando habilitado, o Bay injeta HTTP(S)_PROXY e NO_PROXY nos contêineres de sandbox.
proxy:
  enabled: false
  # http_proxy: "http://proxy.example.com:7890"
  # https_proxy: "http://proxy.example.com:7890"
  # no_proxy: "my-internal.service"

# Pool aquecido: mantém sandboxes de prontidão para reduzir a latência de inicialização.
# Quando um usuário cria uma sandbox, o Bay tenta primeiro utilizar uma instância já aquecida.
warm_pool:
  enabled: true
  # Número de workers da fila de aquecimento
  warmup_queue_workers: 2
  # Tamanho máximo da fila de aquecimento
  warmup_queue_max_size: 256
  # Política aplicada quando a fila está cheia
  warmup_queue_drop_policy: "drop_newest"
  # Limite útil para alertas operacionais
  warmup_queue_drop_alert_threshold: 50
  # Intervalo de manutenção do pool aquecido (segundos)
  interval_seconds: 30
  # Define se a manutenção do pool aquecido será iniciada junto com o Bay
  run_on_startup: true

profiles:
  # ── Sandbox Python padrão ──────────────────────────
  - id: python-default
    description: "Sandbox Python padrão com acesso ao sistema de arquivos e ao Shell"
    image: "ghcr.io/astrbotdevs/shipyard-neo-ship:latest"
    runtime_type: ship
    runtime_port: 8123
    resources:
      cpus: 1.0
      memory: "1g"
    capabilities:
      - filesystem  # inclui upload/download
      - shell
      - python
    # Tempo limite de inatividade (segundos)
    idle_timeout: 1800
    # Mantém 1 instância aquecida pronta
    warm_pool_size: 1
    env: {}
    # Substituição opcional do proxy no nível do perfil
    # proxy:
    #   enabled: false

  # ── Sandbox para ciência de dados (mais recursos) ──
  - id: python-data
    description: "Sandbox para ciência de dados com CPU e memória adicionais"
    image: "ghcr.io/astrbotdevs/shipyard-neo-ship:latest"
    runtime_type: ship
    runtime_port: 8123
    resources:
      cpus: 2.0
      memory: "4g"
    capabilities:
      - filesystem  # inclui upload/download
      - shell
      - python
    idle_timeout: 1800
    warm_pool_size: 1
    env: {}

  # ── Sandbox com navegador e Python em vários contêineres ──
  - id: browser-python
    description: "Automação de navegador com backend Python"
    containers:
      - name: ship
        image: "ghcr.io/astrbotdevs/shipyard-neo-ship:latest"
        runtime_type: ship
        runtime_port: 8123
        resources:
          cpus: 1.0
          memory: "1g"
        capabilities:
          - python
          - shell
          - filesystem  # inclui upload/download
        # Esses recursos são tratados principalmente pelo contêiner ship
        primary_for:
          - filesystem
          - python
          - shell
        env: {}
      - name: browser
        image: "ghcr.io/astrbotdevs/shipyard-neo-gull:latest"
        runtime_type: gull
        runtime_port: 8115
        resources:
          cpus: 1.0
          memory: "2g"
        capabilities:
          - browser
        env: {}
    idle_timeout: 1800
    warm_pool_size: 1

gc:
  # A coleta de lixo automática é recomendada em produção
  enabled: true
  run_on_startup: true
  # Intervalo da coleta de lixo (segundos)
  interval_seconds: 300

  # Deve ser exclusivo em implantações com várias instâncias
  instance_id: "bay-prod"

  idle_session:
    enabled: true
  expired_sandbox:
    enabled: true
  orphan_cargo:
    enabled: true
  orphan_container:
    # Recomendado em produção para limpar contêineres órfãos
    enabled: true
```

Uma forma prática de entender esse arquivo:

- **Alteração mínima obrigatória**: `security.api_key`.
- **Opções ajustadas com mais frequência**: limites de recursos, `warm_pool_size` e `idle_timeout` dentro de `profiles`.
- **Se precisar do recurso de navegador**: use ou personalize o perfil `browser-python`.
- **Se quiser reduzir o tempo de inicialização**: mantenha `warm_pool.enabled: true` e aumente `warm_pool_size` nos perfis usados com frequência.
- **Se os recursos forem limitados**: reduza `warm_pool_size` ou até desabilite `warm_pool`.
- **Se precisar de acesso a um proxy de saída**: configure o `proxy` de nível superior ou substitua a configuração por perfil.

#### Sobre reutilização e persistência no Shipyard Neo

O `Shipyard Neo` possui alguns conceitos importantes:

- **Sandbox**: a unidade de recurso estável e visível externamente.
- **Session**: a sessão real do contêiner em execução, que pode ser interrompida ou recriada.
- **Cargo**: o volume persistente do espaço de trabalho, montado em `/workspace`.

Do ponto de vista do AstrBot, a implementação atual armazena em cache o inicializador da sandbox com base no `session_id` da solicitação; no fluxo padrão do agente principal, esse `session_id` geralmente é igual ao identificador da sessão de mensagens `unified_msg_origin`. Como resultado, solicitações subsequentes da mesma sessão de mensagens normalmente continuam usando a mesma sandbox Neo; se a sandbox ficar indisponível, ela será recriada automaticamente.

Para explicações mais detalhadas sobre TTL e persistência, consulte as seções posteriores sobre “`Shipyard Neo Sandbox TTL`” e “Persistência de dados no ambiente de sandbox”.

#### Configurar o Shipyard Neo

Se você escolher o `Shipyard Neo`, os principais itens de configuração são:

- `Shipyard Neo API Endpoint`
  - Para uma implantação conjunta, use `http://bay:8114`.
  - Para uma implantação separada, use o endereço real, como `http://<your-host>:8114`.
- `Shipyard Neo Access Token`
  - Informe a chave de API do Bay.
  - Em uma implantação conjunta oficial, se o AstrBot puder acessar o arquivo `credentials.json` do Bay, você poderá deixar o campo vazio para descoberta automática.
- `Shipyard Neo Profile`
  - Por exemplo, `python-default` ou `browser-python`.
  - Se ficar vazio, o AstrBot tentará escolher um perfil com recursos mais completos, dando preferência a um que inclua o recurso `browser`, e usará `python-default` como alternativa, se necessário.
- `Shipyard Neo Sandbox TTL`
  - O limite máximo de duração da sandbox, cujo padrão é 3600 segundos (1 hora).

#### Sobre `Shipyard Neo Sandbox TTL`

No `Shipyard Neo`:

- TTL representa o limite máximo de duração da sandbox.
- O perfil selecionado também define um tempo limite de inatividade separado (`idle_timeout`).
- As chamadas de recursos feitas pelo AstrBot geralmente renovam o tempo limite de inatividade, em vez de estender diretamente o TTL.
- `keepalive` estende apenas o tempo limite de inatividade; não inicia automaticamente uma nova sessão nem estende o TTL.

<span id="about-data-persistence-in-the-sandbox-environment"></span>

#### Persistência de dados {#shipyard-neo-persistence}

A raiz do espaço de trabalho do `Shipyard Neo` é fixa em `/workspace`.

A persistência é fornecida pelo Cargo:

- Os dados do sistema de arquivos são armazenados no Cargo e montados em `/workspace`.
- Mesmo que a Session subjacente seja interrompida ou recriada, os dados no Cargo geralmente são mantidos.
- Em perfis com recurso de navegador, o estado do navegador também pode ser persistido, por exemplo, em `/workspace/.browser/profile/`.

<span id="cua-runtime"></span>

### CUA {#cua}

O [CUA](https://github.com/trycua/cua) é um ambiente de execução de sandbox para Computer Use.

O Agent pode usar as seguintes ferramentas em uma sandbox CUA. A disponibilidade real depende da imagem e do ambiente de execução selecionados:

| Recurso | Ferramenta disponibilizada ao Agent | Finalidade |
| --- | --- | --- |
| Execução de Shell | `astrbot_execute_shell` | Executar comandos e iniciar programas |
| Execução de Python | `astrbot_execute_ipython` | Executar código Python |
| Leitura de arquivos | `astrbot_file_read_tool` | Ler arquivos |
| Gravação de arquivos | `astrbot_file_write_tool` | Criar ou sobrescrever arquivos |
| Edição de arquivos | `astrbot_file_edit_tool` | Substituir um trecho especificado em arquivos |
| Pesquisa em arquivos | `astrbot_grep_tool` | Pesquisar conteúdo de arquivos por padrão |
| Envio de arquivos | `astrbot_upload_file` | Enviar arquivos do ambiente que executa o AstrBot para a sandbox |
| Download de arquivos | `astrbot_download_file` | Baixar arquivos da sandbox, com a opção de enviá-los ao usuário |
| Captura de tela da área de trabalho | `astrbot_cua_screenshot` | Capturar uma tela para inspeção pelo modelo ou enviá-la ao usuário |
| Clique do mouse | `astrbot_cua_mouse_click` | Clicar em coordenadas com um botão específico do mouse |
| Entrada pelo teclado | `astrbot_cua_keyboard_type` | Digitar texto no controle que estiver em foco |

> [!WARNING]
> O CUA é opcional e não é instalado por padrão com o AstrBot. Se você selecionar CUA sem instalar o pacote `cua` no ambiente Python do AstrBot, a inicialização da sandbox informará que a dependência está ausente.

#### Quando escolher CUA

Escolha CUA quando você:

- Precisar de automação de interface gráfica, incluindo capturas de tela da área de trabalho, cliques do mouse e entrada pelo teclado.
- Precisar testar o comportamento em imagens de diferentes sistemas operacionais, como Linux, Windows e Android.
- Já tiver um ambiente de execução CUA local ou na nuvem implantado.

Se precisar apenas de uma sandbox confiável de Python/Shell/sistema de arquivos, sem interação com a interface gráfica da área de trabalho, prefira o Shipyard Neo. Ele se integra melhor ao espaço de trabalho do AstrBot, à sincronização de Skills e ao uso prolongado.

#### Instalar as dependências do CUA

Na WebUI, abra **Dados e logs → Logs** (`Data & Logs → Logs`), clique em **Instalar pacote Pip** (`Install Pip Package`) e informe `cua` para instalar a dependência. Você também pode instalá-la diretamente no ambiente Python do AstrBot:

- Para implantações a partir do código-fonte ou em ambiente virtual:

  ```bash
  pip install cua
  ```

- Para ambientes do AstrBot gerenciados com `uv`, execute no diretório do projeto:

  ```bash
  uv pip install cua
  ```

O CUA também possui requisitos específicos para seu ambiente de execução:

- Contêineres Linux locais geralmente exigem Docker.
- Máquinas virtuais Linux/Windows locais geralmente exigem QEMU ou o ambiente de execução CUA correspondente.
- Máquinas virtuais macOS geralmente exigem o ambiente de execução CUA/Lume.
- O CUA na nuvem exige uma chave de API CUA.

Consulte a [documentação do CUA](https://cua.ai/docs) para ver os requisitos do host, as imagens compatíveis e as instruções de instalação do ambiente de execução local.

#### Configurar o CUA no AstrBot

Abra **Configuração → IA → Recursos → Agent Computer Use** e defina:

- **Ambiente de execução do Computer Use**: `sandbox` (Sandbox de terceiros).
- **Driver de sandbox**: `CUA`.

As configurações do CUA incluem:

- `CUA Image`: a imagem a iniciar, geralmente `linux`, `macos`, `windows` ou `android`. Padrão: `linux`.
- `CUA OS Type`: o sistema operacional da imagem. Padrão: `linux`. Essa opção determina se o AstrBot pode usar alternativas de Shell POSIX.
- `CUA Sandbox TTL`: duração da sandbox em segundos. Padrão: `3600`.
- `CUA Telemetry Enabled`: define se a telemetria do CUA está habilitada. Desabilitada por padrão.
- `CUA Local Runtime`: define se o ambiente de execução local será usado. Habilitado por padrão. Desabilite-o para usar o ambiente de execução na nuvem do SDK CUA.
- `CUA API Key`: a chave de API do CUA na nuvem. Informe-a somente ao usar o ambiente de execução na nuvem.

Uma configuração mínima para um contêiner Linux local é:

```text
Computer Use Runtime = sandbox
Sandbox Driver = CUA
CUA Image = linux
CUA OS Type = linux
CUA Local Runtime = true
CUA Sandbox TTL = 3600
```

Para usar o CUA na nuvem, utilize:

```text
Computer Use Runtime = sandbox
Sandbox Driver = CUA
CUA Image = linux
CUA OS Type = linux
CUA Local Runtime = false
CUA API Key = <your-cua-api-key>
```

> [!WARNING]
> Não inclua a chave de API do CUA em logs públicos, capturas de tela ou issues.

#### Observações sobre o uso do CUA

- A imagem `linux` geralmente é adequada para testes de Shell, Python, sistema de arquivos e automação da área de trabalho.
- Imagens que não são POSIX, como `windows` e `android`, talvez não ofereçam suporte a comandos como `sh`, `cat`, `ls`, `rm` ou `base64`. O AstrBot retorna erros explícitos para operações alternativas que dependem de comandos indisponíveis.
- Para abrir um navegador ou aplicativo gráfico na sandbox, use a execução em segundo plano do Shell quando houver suporte, por exemplo, `background=true`, para evitar bloquear chamadas subsequentes de ferramentas.
- Enviar diretamente ao usuário um caminho de arquivo da sandbox geralmente não funciona. Use a ferramenta de download da sandbox do AstrBot para baixar o arquivo para o diretório temporário do AstrBot antes de enviá-lo.
- CUA e Shipyard Neo têm semânticas diferentes para o espaço de trabalho. O Shipyard Neo usa uma raiz fixa `/workspace`; o diretório de trabalho e os caminhos do CUA dependem da imagem e do ambiente de execução.

<span id="legacy-option-shipyard"></span>

### Shipyard (legado) {#shipyard}

O conteúdo a seguir descreve o driver antigo `Shipyard`. Ele é mantido para compatibilidade com implantações legadas existentes.

#### Implantar o AstrBot e o Shipyard com Docker Compose

Se você ainda não implantou o AstrBot ou deseja usar o método de implantação antigo, anteriormente recomendado e com suporte a sandbox, ainda poderá implantar o AstrBot com Docker Compose usando os comandos abaixo:

```bash
git clone https://github.com/AstrBotDevs/AstrBot
cd AstrBot
# Altere as variáveis de ambiente em compose-with-shipyard.yml, como o token de acesso do Shipyard
docker compose -f compose-with-shipyard.yml up -d
docker pull soulter/shipyard-ship:latest
```

Isso inicia uma pilha Docker Compose contendo o programa principal do AstrBot e o ambiente de sandbox.

#### Implantar o Shipyard separadamente

Se o AstrBot já estiver implantado, mas o ambiente de sandbox ainda não estiver, você poderá implantar o Shipyard separadamente.

```bash
mkdir astrbot-shipyard
cd astrbot-shipyard
wget https://raw.githubusercontent.com/AstrBotDevs/shipyard/refs/heads/main/pkgs/bay/docker-compose.yml -O docker-compose.yml
# Altere as variáveis de ambiente em docker-compose.yml, como o token de acesso do Shipyard
docker compose -f docker-compose.yml up -d
docker pull soulter/shipyard-ship:latest
```

Após a implantação bem-sucedida, o Shipyard escuta por padrão em `http://<your-host>:8156`.

> [!TIP]
> Se você implantar o AstrBot com Docker, também poderá colocar o Shipyard na mesma rede Docker do AstrBot, evitando a necessidade de publicar a porta do Shipyard no host.

#### Configurar o Shipyard (legado)

Se você escolher o driver legado `Shipyard`, os itens de configuração relevantes serão:

- `Shipyard API Endpoint`
  - Se usar a implantação Docker Compose acima, defina como `http://shipyard:8156`.
  - Se o Shipyard estiver implantado separadamente, use o endereço correspondente, como `http://<your-host>:8156`.
- `Shipyard Access Token`
  - Informe o token de acesso configurado durante a implantação do Shipyard.
- `Shipyard Ship Lifetime (seconds)`
  - Define o tempo de vida de cada instância de sandbox. O padrão é 3600 segundos (1 hora).
- `Shipyard Ship Session Reuse Limit`
  - Define o número máximo de sessões que podem reutilizar a mesma instância de sandbox. O padrão é 10.

#### Sobre `Shipyard Ship Lifetime (seconds)`

A explicação a seguir se aplica somente ao driver legado `Shipyard`:

O tempo de vida de uma instância de sandbox define o período máximo durante o qual ela pode existir antes de ser destruída. Esse valor deve ser escolhido de acordo com seu caso de uso e os recursos disponíveis.

- Quando uma nova sessão entra em uma instância de sandbox existente, a instância estende automaticamente seu tempo de vida para o TTL solicitado por essa sessão.
- Quando uma operação é realizada em uma instância de sandbox, a instância estende automaticamente seu tempo de vida para o horário atual mais o TTL.

#### Persistência de dados {#shipyard-persistence}

O Shipyard aloca um diretório de trabalho para cada sessão em `/home/<unique session ID>`.

O Shipyard monta automaticamente o diretório `/home` do ambiente de sandbox em `${PWD}/data/shipyard/ship_mnt_data` no host. Quando uma instância de sandbox é destruída e uma sessão solicita a sandbox novamente mais tarde, o Shipyard recria uma nova instância e monta novamente os dados persistidos anteriormente para preservar a continuidade.
