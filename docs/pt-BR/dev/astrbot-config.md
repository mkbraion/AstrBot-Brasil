---
outline: deep
---

# Arquivo de configuração do AstrBot

## data/cmd_config.json

O arquivo de configuração do AstrBot está no formato JSON. O AstrBot lê esse arquivo ao iniciar e inicializa o sistema com base nas configurações definidas nele. Seu caminho é `data/cmd_config.json`.

> A partir do AstrBot v4.0.0, foi introduzido o conceito de [múltiplos arquivos de configuração](https://blog.astrbot.app/posts/what-is-changed-in-4.0.0/#%E5%A4%9A%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6). O arquivo `data/cmd_config.json` funciona como a configuração padrão, chamada `default`. Os demais arquivos de configuração criados na WebUI são armazenados no diretório `data/config/` e começam com o prefixo `abconf_`.

Na WebUI, gerencie os perfis de comportamento do bot e das sessões (incluindo texto para imagem) em `Config`. As configurações globais de execução, registro de logs, rede e segurança da WebUI ficam em `System Settings`. As conexões com modelos e bots são gerenciadas, respectivamente, em `Providers` e `Platforms`.

A configuração padrão do AstrBot é a seguinte:

```jsonc
{
    "config_version": 2,
    "platform_settings": {
        "unique_session": False,
        "rate_limit": {
            "time": 60,
            "count": 30,
            "strategy": "stall",  # stall, discard
        },
        "reply_prefix": "",
        "forward_threshold": 1500,
        "enable_id_white_list": True,
        "id_whitelist": [],
        "id_whitelist_log": True,
        "wl_ignore_admin_on_group": True,
        "wl_ignore_admin_on_friend": True,
        "reply_with_mention": False,
        "reply_with_quote": False,
        "path_mapping": [],
        "segmented_reply": {
            "enable": False,
            "only_llm_result": True,
            "interval_method": "random",
            "interval": "1.5,3.5",
            "log_base": 2.6,
            "words_count_threshold": 150,
            "regex": ".*?[。？！~…]+|.+$",
            "content_cleanup_rule": "",
        },
        "no_permission_reply": True,
        "empty_mention_waiting": True,
        "empty_mention_waiting_need_reply": True,
        "friend_message_needs_wake_prefix": False,
        "ignore_bot_self_message": False,
        "ignore_at_all": False,
    },
    "provider": [],
    "provider_settings": {
        "enable": True,
        "default_provider_id": "",
        "default_image_caption_provider_id": "",
        "image_caption_prompt": "Please describe the image using Chinese.",
        "provider_pool": ["*"],  # "*" means use all available providers
        "wake_prefix": "",
        "web_search": False,
        "websearch_provider": "tavily",
        "websearch_tavily_key": [],
        "websearch_bocha_key": [],
        "websearch_brave_key": [],
        "web_search_link": False,
        "display_reasoning_text": False,
        "identifier": False,
        "group_name_display": False,
        "datetime_system_prompt": True,
        "default_personality": "default",
        "persona_pool": ["*"],
        "prompt_prefix": "{{prompt}}",
        "max_context_length": -1,
        "dequeue_context_length": 1,
        "streaming_response": False,
        "show_tool_use_status": False,
        "streaming_segmented": False,
        "max_agent_step": 128,
        "tool_call_timeout": 120,
    },
    "provider_stt_settings": {
        "enable": False,
        "provider_id": "",
    },
    "provider_tts_settings": {
        "enable": False,
        "provider_id": "",
        "dual_output": False,
        "use_file_service": False,
    },
    "provider_ltm_settings": {
        "group_icl_enable": False,
        "group_message_max_cnt": 1000,
        "image_caption": False,
        "active_reply": {
            "enable": False,
            "method": "possibility_reply",
            "possibility_reply": 0.1,
            "whitelist": [],
        },
    },
    "content_safety": {
        "also_use_in_response": False,
        "internal_keywords": {"enable": True, "extra_keywords": []},
        "baidu_aip": {"enable": False, "app_id": "", "api_key": "", "secret_key": ""},
    },
    "admins_id": ["astrbot"],
    "t2i": False,
    "t2i_word_threshold": 150,
    "t2i_strategy": "remote",
    "t2i_endpoint": "",
    "t2i_use_file_service": False,
    "t2i_active_template": "base",
    "http_proxy": "",
    "no_proxy": ["localhost", "127.0.0.1", "::1"],
    "dashboard": {
        "enable": True,
        "username": "astrbot",
        "password": "<your_password_md5>",
        "jwt_secret": "",
        "host": "0.0.0.0",
        "port": 6185,
    },
    "platform": [],
    "platform_specific": {
        # Platform-specific settings: categorized by platform, then by feature group
        "lark": {
            "pre_ack_emoji": {"enable": False, "emojis": ["Typing"]},
        },
        "telegram": {
            "pre_ack_emoji": {"enable": False, "emojis": ["✍️"]},
        },
        "discord": {
            "pre_ack_emoji": {"enable": False, "emojis": ["🤔"]},
        },
    },
    "wake_prefix": ["/"],
    "log_level": "INFO",
    "trace_enable": False,
    "pip_install_arg": "",
    "pypi_index_url": "https://mirrors.aliyun.com/pypi/simple/",
    "persona": [],  # deprecated
    "timezone": "Asia/Shanghai",
    "callback_api_base": "",
    "default_kb_collection": "",  # Default knowledge base name
    "plugin_set": ["*"],  # "*" means use all available plugins, empty list means none
}
```

## Detalhes dos campos

### `config_version`

Versão da configuração. Não altere este valor.

### `platform_settings`

Configurações gerais dos adaptadores de plataformas de mensagens.

#### `platform_settings.unique_session`

Define se o recurso **Isolar conversa** deve ser ativado. O padrão é `false`. Nas plataformas compatíveis, quando esse recurso está ativado, cada integrante de um grupo possui um contexto de conversa separado. Nas plataformas não compatíveis, o contexto existente é mantido. O acesso aos comandos `/new` e `/reset` é controlado pelas [permissões de comandos](../use/command.md), que, por padrão, seguem o isolamento de conversas.

#### `platform_settings.rate_limit`

Estratégia aplicada quando a taxa de mensagens ultrapassa os limites. `time` define a janela de tempo, `count` define a quantidade de mensagens e `strategy` define a estratégia de limitação. `stall` significa aguardar; `discard` significa descartar.

#### `platform_settings.reply_prefix`

Texto de prefixo fixo usado nas respostas às mensagens. O padrão é uma string vazia.

#### `platform_settings.forward_threshold`

> Atualmente, esta opção se aplica somente ao adaptador da plataforma QQ.

Limite para encaminhamento de mensagens. Quando o conteúdo da resposta ultrapassa determinada quantidade de caracteres, o bot agrupa a mensagem em uma "mensagem encaminhada" de grupo do QQ para evitar o envio excessivo de mensagens.

Na WebUI, selecione o perfil usado pelo bot e abra `Access Control → Whitelist` para gerenciar as configurações de lista de permissões a seguir.

#### `platform_settings.enable_id_white_list`

Define se a lista de permissões por ID será ativada. O padrão é `true`. Quando ativada, somente mensagens provenientes de IDs presentes na lista serão processadas.

#### `platform_settings.id_whitelist`

Lista de permissões por ID. Quando preenchida, somente eventos de mensagem dos IDs especificados serão processados. Se estiver vazia, o filtro da lista de permissões não será aplicado. Você pode usar o comando `/sid` para obter o ID da sessão em uma plataforma.

Os IDs de sessão também podem ser encontrados nos logs do AstrBot. Quando uma mensagem não passa pelo filtro da lista de permissões, é gerado um log de nível INFO, por exemplo: `aiocqhttp:GroupMessage:547540978`.

#### `platform_settings.id_whitelist_log`

Define se serão registrados logs das mensagens que não passam pelo filtro da lista de permissões por ID. O padrão é `true`.

#### `platform_settings.wl_ignore_admin_on_group` e `platform_settings.wl_ignore_admin_on_friend`

- `wl_ignore_admin_on_group`: define se mensagens de administradores em grupos ignoram a lista de permissões por ID. O padrão é `true`.
- `wl_ignore_admin_on_friend`: define se mensagens privadas de administradores ignoram a lista de permissões por ID. O padrão é `true`.

#### `platform_settings.reply_with_mention`

Define se o usuário será mencionado com @ ao receber uma resposta. O padrão é `false`.

#### `platform_settings.reply_with_quote`

Define se a mensagem do usuário será citada na resposta. O padrão é `false`.

#### `platform_settings.path_mapping`

*Este item de configuração está obsoleto desde a versão v4.0.0.*

Lista de mapeamentos de caminhos. É usada para substituir caminhos de arquivos nas mensagens. Cada item de mapeamento contém os campos `from` e `to`, indicando que o trecho `from` do caminho presente na mensagem será substituído por `to`.

#### `platform_settings.segmented_reply`

Configurações de respostas segmentadas.

- `enable`: define se as respostas segmentadas serão ativadas. O padrão é `false`.
- `only_llm_result`: define se somente respostas geradas pelo LLM serão segmentadas. O padrão é `true`.
- `interval_method`: método usado para determinar os intervalos entre segmentos. As opções são `random` e `log`. O padrão é `random`.
- `interval`: intervalo de tempo entre segmentos. Para `random`, informe dois números separados por vírgula, representando os intervalos mínimo e máximo em segundos. Para `log`, informe um número que represente a base do logaritmo. O padrão é `"1.5,3.5"`.
- `log_base`: base do logaritmo, aplicável somente quando `interval_method` é `log`. O padrão é `2.6`.
- `words_count_threshold`: limite de caracteres para respostas segmentadas. Somente mensagens menores que esse valor serão segmentadas; mensagens mais longas serão enviadas diretamente, sem segmentação. O padrão é `150`.
- `regex`: expressão regular usada para dividir uma mensagem. Por padrão, a divisão considera sinais de pontuação, como pontos e interrogações. A operação é `re.findall(r'<regex>', text)`. O padrão é `".*?[。？！~…]+|.+$"`.
- `content_cleanup_rule`: remove conteúdos especificados dos segmentos. Aceita expressões regulares. Por exemplo, `[。？！]` remove pontos, interrogações e pontos de exclamação. A operação é `re.sub(r'<regex>', '', text)`.

#### `platform_settings.no_permission_reply`

Define se será enviada uma mensagem de falta de permissão quando um usuário não tiver autoridade suficiente. O padrão é `true`.

#### `platform_settings.empty_mention_waiting`

Define se o mecanismo de espera após uma menção vazia com @ será ativado. O padrão é `true`. Quando ativado, se um usuário enviar uma mensagem contendo somente uma menção ao bot, o bot aguardará até 60 segundos para que o usuário envie a mensagem seguinte e combinará as duas mensagens para processamento. Esse recurso é especialmente útil em plataformas que não permitem enviar uma menção com @ junto de áudio ou imagens.

#### `platform_settings.empty_mention_waiting_need_reply`

No mecanismo descrito em `empty_mention_waiting`, quando a espera for acionada, esta opção define se o bot deverá gerar imediatamente uma resposta usando o LLM. Se estiver desativada, o bot apenas aguardará, sem responder. O padrão é `true`.

#### `platform_settings.friend_message_needs_wake_prefix`

Define se mensagens privadas nas plataformas exigem um prefixo de ativação. O padrão é `false`. Quando ativada, os usuários precisam incluir um prefixo de ativação para acionar uma resposta do bot em conversas privadas.

#### `platform_settings.ignore_bot_self_message`

Define se as mensagens enviadas pelo próprio bot serão ignoradas. O padrão é `false`. Quando ativada, o bot não processará as próprias mensagens, evitando loops infinitos em algumas plataformas.

#### `platform_settings.ignore_at_all`

Define se mensagens com menção a todos (`@all`) serão ignoradas. O padrão é `false`. Quando ativada, o bot não responderá a mensagens que contenham `@all`.

### `provider`

> Este item produz efeito somente em `data/cmd_config.json`; o AstrBot não o lê nos arquivos de configuração do diretório `data/config/`.

Lista das configurações dos provedores de serviços de modelos.

### `provider_settings`

Configurações gerais dos provedores de LLM.

#### `provider_settings.enable`

Define se o chat com LLM será ativado. O padrão é `true`.

#### `provider_settings.default_provider_id`

ID do provedor de modelo padrão para conversas. Deve ser um ID de provedor já configurado na lista `provider`. Se estiver vazio, será usado o primeiro provedor da lista.

#### `provider_settings.default_image_caption_provider_id`

ID do provedor de modelo padrão para descrição de imagens. Deve ser um ID de provedor já configurado na lista `provider`. Se estiver vazio, a descrição de imagens será desativada.

Isso significa que, quando um usuário enviar uma imagem, o AstrBot usará esse provedor para gerar uma descrição em texto, que será incorporada ao contexto da conversa. Esse recurso é útil quando o modelo usado na conversa não oferece suporte a entradas multimodais.

#### `provider_settings.image_caption_prompt`

Modelo de prompt usado para descrever imagens. O padrão é `"Please describe the image using Chinese."`.

#### `provider_settings.provider_pool`

*Este item de configuração ainda não está em uso efetivo.*

#### `provider_settings.wake_prefix`

Condição adicional para acionar o chat com LLM. Por exemplo, se o valor for `chat`, as mensagens deverão começar com `/chat` para acionar o chat com LLM, sendo `/` o prefixo de ativação do bot. Essa medida ajuda a evitar abusos.

#### `provider_settings.web_search`

Define se o recurso integrado de pesquisa na Web do AstrBot será ativado. O padrão é `false`. Quando ativado, o LLM poderá pesquisar automaticamente na Web e responder com base no conteúdo encontrado.

#### `provider_settings.websearch_provider`

Tipo de provedor de pesquisa na Web. O padrão é `tavily`. Atualmente, são aceitos `tavily`, `bocha`, `baidu_ai_search`, `brave` e `firecrawl`.

- `tavily`: usa o mecanismo de pesquisa Tavily.
- `bocha`: usa o mecanismo de pesquisa BoCha.
- `baidu_ai_search`: usa o Baidu AI Search (MCP).
- `brave`: usa a API Brave Search.
- `firecrawl`: usa a API Firecrawl Search.

#### `provider_settings.websearch_tavily_key`

Lista de chaves de API do mecanismo de pesquisa Tavily. É obrigatória quando `tavily` é usado como provedor de pesquisa na Web.

#### `provider_settings.websearch_bocha_key`

Lista de chaves de API do mecanismo de pesquisa BoCha. É obrigatória quando `bocha` é usado como provedor de pesquisa na Web.

#### `provider_settings.websearch_brave_key`

Lista de chaves de API do Brave Search. É obrigatória quando `brave` é usado como provedor de pesquisa na Web.

#### `provider_settings.websearch_firecrawl_key`

Lista de chaves de API do Firecrawl Search. É obrigatória quando `firecrawl` é usado como provedor de pesquisa na Web.

#### `provider_settings.web_search_link`

Define se o modelo será instruído a incluir links para os resultados da pesquisa na resposta. O padrão é `false`.

#### `provider_settings.display_reasoning_text`

Define se o processo de raciocínio do modelo será exibido na resposta. O padrão é `false`.

#### `provider_settings.identifier`

Define se o nome do integrante do grupo será acrescentado ao prompt para ajudar o modelo a compreender o contexto da conversa em grupo. O padrão é `false`. Ativar esta opção aumenta ligeiramente o consumo de tokens.

#### `provider_settings.group_name_display`

Define se o modelo será informado sobre o nome do grupo em que está. O padrão é `false`. Atualmente, esta opção produz efeito somente no adaptador da plataforma QQ.

#### `provider_settings.datetime_system_prompt`

Define se a data e a hora atuais da máquina serão incluídas no prompt de sistema. O padrão é `true`.

#### `provider_settings.default_personality`

ID da personalidade padrão a ser usada. Configure as personalidades na WebUI.

#### `provider_settings.persona_pool`

*Este item de configuração ainda não está em uso efetivo.*

#### `provider_settings.prompt_prefix`

Prompt do usuário. Você pode usar `{{prompt}}` como placeholder para a entrada do usuário. Se nenhum placeholder for informado, o conteúdo será acrescentado antes da entrada do usuário.

#### `provider_settings.max_context_length`

Quando o contexto da conversa ultrapassar esse valor, as partes mais antigas serão descartadas. Cada rodada de conversa conta como 1. O valor -1 significa que não há limite.

#### `provider_settings.dequeue_context_length`

Quantidade de rodadas de conversa descartadas sempre que o limite de `max_context_length` for atingido.

#### `provider_settings.streaming_response`

Define se as respostas em streaming serão ativadas. O padrão é `false`. Quando ativadas, as respostas do modelo são enviadas ao usuário em tempo real, com efeito de digitação. Esta opção produz efeito somente nas plataformas WebChat, Telegram e Lark.

#### `provider_settings.show_tool_use_status`

Define se o status de uso de ferramentas será exibido. O padrão é `false`. Quando ativada, o modelo exibe o nome da ferramenta e os parâmetros de entrada ao utilizá-la.

#### `provider_settings.streaming_segmented`

Define se plataformas sem suporte a respostas em streaming deverão recorrer a respostas segmentadas. O padrão é `false`. Assim, se o streaming estiver ativado, mas a plataforma não for compatível, serão usadas várias respostas segmentadas.

#### `provider_settings.max_agent_step`

Limite máximo de etapas do Agent. O padrão é `128`. Cada chamada de ferramenta realizada pelo modelo conta como uma etapa.

#### `provider_settings.tool_call_timeout`

Adicionado na versão `v4.3.5`.

Tempo limite máximo para chamadas de ferramentas, em segundos. O padrão é `60` segundos.

### `provider_stt_settings`

Configurações gerais dos provedores de conversão de fala em texto (STT).

#### `provider_stt_settings.enable`

Define se os serviços de STT serão ativados. O padrão é `false`.

#### `provider_stt_settings.provider_id`

ID do provedor de STT. Deve ser um ID de provedor de STT já configurado na lista `provider`.

### `provider_tts_settings`

Configurações gerais dos provedores de conversão de texto em fala (TTS).

#### `provider_tts_settings.enable`

Define se os serviços de TTS serão ativados. O padrão é `false`.

#### `provider_tts_settings.provider_id`

ID do provedor de TTS. Deve ser um ID de provedor de TTS já configurado na lista `provider`.

#### `provider_tts_settings.dual_output`

Define se a saída dupla será ativada. O padrão é `false`. Quando ativada, o bot envia mensagens de texto e de voz.

#### `provider_tts_settings.use_file_service`

Define se o serviço de arquivos será ativado. O padrão é `false`. Quando ativado, o bot fornece o arquivo de áudio gerado à plataforma de mensagens por meio de um link HTTP externo. Esse recurso depende da configuração `callback_api_base`.

### `provider_ltm_settings`

Configurações gerais dos provedores de reconhecimento de contexto de conversas em grupo.

#### `provider_ltm_settings.group_icl_enable`

Define se os registros de conversas em grupo serão inseridos no contexto do modelo. O padrão é `false`. Quando ativada, o bot registra temporariamente as mensagens do grupo e as insere no contexto da próxima resposta.

O conteúdo do contexto é colocado no prompt de sistema da conversa.

#### `provider_ltm_settings.group_message_max_cnt`

Quantidade máxima de mensagens de conversas em grupo mantidas para inserção no contexto. O padrão é `1000`. Mensagens que ultrapassarem essa quantidade serão descartadas. Esta opção só se aplica quando a inserção de registros de conversas em grupo está ativada.

#### `provider_ltm_settings.image_caption`

Define se as imagens das conversas em grupo serão descritas automaticamente e se as descrições serão inseridas no contexto. O padrão é `false`. Esta opção só se aplica quando a inserção de registros de conversas em grupo está ativada. Use-a com cautela, pois ela pode aumentar significativamente a quantidade de chamadas de API e o consumo de tokens.

#### `provider_ltm_settings.active_reply`

- `enable`: define se as respostas proativas serão ativadas. O padrão é `false`.
- `method`: método usado para respostas proativas. A opção disponível é `possibility_reply`.
- `possibility_reply`: probabilidade de uma resposta proativa. O padrão é `0.1`. Aplica-se somente quando `method` é `possibility_reply`.
- `whitelist`: lista de permissões por ID para respostas proativas. Somente IDs presentes nessa lista poderão acionar respostas proativas. Se estiver vazia, nenhum filtro de lista de permissões será aplicado. Você pode usar o comando `/sid` para obter o ID da sessão em uma plataforma.

### `content_safety`

Configurações de segurança de conteúdo.

#### `content_safety.also_use_in_response`

Define se as respostas do LLM também passarão por verificações de segurança de conteúdo. O padrão é `false`. Quando ativada, as respostas geradas pelo bot também são verificadas para evitar conteúdo inadequado.

#### `content_safety.internal_keywords`

Configurações de detecção de palavras-chave internas.

- `enable`: define se a detecção de palavras-chave internas será ativada. O padrão é `true`.
- `extra_keywords`: lista de palavras-chave adicionais. Aceita expressões regulares. O padrão é uma lista vazia.

#### `content_safety.baidu_aip`

Configurações de moderação de conteúdo do Baidu AI.

- `enable`: define se a moderação de conteúdo do Baidu AI será ativada. O padrão é `false`.
- `app_id`: ID do aplicativo para a moderação de conteúdo do Baidu AI.
- `api_key`: chave de API para a moderação de conteúdo do Baidu AI.
- `secret_key`: chave secreta para a moderação de conteúdo do Baidu AI.

> [!TIP]
> Para ativar a moderação de conteúdo do Baidu AI, instale primeiro o pacote com `pip install baidu-aip`.

### `admins_id`

Lista de IDs de administradores. Além disso, você pode usar os comandos `/op` e `/deop` para adicionar ou remover administradores.

Na WebUI, selecione o perfil usado pelo bot em `Config` e abra `Access Control → Administrators → Administrator IDs`. Envie `/sid` ao bot para obter seu `UID`.

### `t2i`

Define se a funcionalidade de texto para imagem (T2I) será ativada. O padrão é `false`. Quando ativada, se a mensagem de um usuário ultrapassar determinada quantidade de caracteres, o bot a renderizará como imagem para melhorar a legibilidade e evitar o envio excessivo de mensagens. Há suporte à renderização de Markdown.

### `t2i_word_threshold`

Limite de caracteres para T2I. O padrão é `150`. Quando uma mensagem ultrapassa essa quantidade, o bot a renderiza como imagem.

### `t2i_strategy`

Estratégia de renderização para T2I. As opções são `local` e `remote`. O padrão é `remote`.

- `local`: usa o serviço T2I local do AstrBot para renderização. A qualidade é inferior, mas não há dependência de serviços externos.
- `remote`: usa um serviço T2I remoto para renderização. Por padrão, utiliza o serviço oficial do AstrBot, que oferece melhor qualidade.

### `t2i_endpoint`

Endereço da API do AstrBot, usado para renderizar imagens em Markdown. Produz efeito quando `t2i_strategy` é `remote`. O padrão é vazio, o que significa que o serviço oficial do AstrBot será usado.

### `t2i_use_file_service`

Define se o serviço de arquivos será ativado. O padrão é `false`. Quando ativado, o bot fornece a imagem renderizada à plataforma de mensagens por meio de um link HTTP externo. Esse recurso depende da configuração `callback_api_base`.

### `http_proxy`

Proxy HTTP. Por exemplo, `http://localhost:7890`. Quando o AstrBot estiver em execução no Docker, use um endereço acessível a partir do contêiner do AstrBot. Consulte [Implantar com Docker](/en/deploy/astrbot/docker.md).

### `no_proxy`

Lista de endereços que não devem usar o proxy. Por exemplo, `["localhost", "127.0.0.1"]`.

### `dashboard`

Configurações da WebUI do AstrBot.

Não altere o valor de `password` arbitrariamente. Trata-se de uma senha codificada em `md5`, gerada a partir da senha inicial aleatória. Na primeira execução, consulte os logs de inicialização para encontrar essa senha e, em seguida, altere-a no painel de controle.

- `enable`: define se a WebUI do AstrBot será ativada. O padrão é `true`.
- `username`: nome de usuário da WebUI do AstrBot.
- `password`: senha da WebUI do AstrBot. Ela é inicializada a partir de uma senha aleatória gerada na primeira inicialização e registrada nos logs. Não a modifique diretamente, a menos que saiba exatamente o que está fazendo.
- `jwt_secret`: chave secreta JWT. O AstrBot gera esse valor aleatoriamente durante a inicialização. Não o modifique, a menos que saiba exatamente o que está fazendo.
- `host`: endereço no qual a WebUI do AstrBot ficará disponível. O padrão é `0.0.0.0`.
- `port`: porta da WebUI do AstrBot. O padrão é `6185`.

### `platform`

> Este item produz efeito somente em `data/cmd_config.json`; o AstrBot não o lê nos arquivos de configuração do diretório `data/config/`.

Lista das configurações dos adaptadores de plataformas de mensagens do AstrBot.

### `platform_specific`

Configurações específicas de cada plataforma. São organizadas por plataforma e, em seguida, por grupo de funcionalidades.

#### `platform_specific.<platform>.pre_ack_emoji`

Quando ativada, esta opção faz com que o AstrBot envie um emoji antes de solicitar uma resposta ao LLM, informando ao usuário que a solicitação está sendo processada. Atualmente, produz efeito somente nos adaptadores das plataformas Lark e Telegram.

##### lark

- `enable`: define se os emojis de confirmação prévia para mensagens do Lark serão ativados. O padrão é `false`.
- `emojis`: lista de emojis de confirmação prévia. O padrão é `["Typing"]`. Consulte a [documentação de emojis](https://open.feishu.cn/document/server-docs/im-v1/message-reaction/emojis-introduce) para conhecer os nomes disponíveis.

##### telegram

- `enable`: define se os emojis de confirmação prévia para mensagens do Telegram serão ativados. O padrão é `false`.
- `emojis`: lista de emojis de confirmação prévia. O padrão é `["✍️"]`. O Telegram aceita somente um conjunto fixo de reações; consulte o arquivo [reactions.txt](https://gist.github.com/Soulter/3f22c8e5f9c7e152e967e8bc28c97fc9).

##### discord

- `enable`: define se os emojis de confirmação prévia para mensagens do Discord serão ativados. O padrão é `false`.
- `emojis`: lista de emojis de confirmação prévia. O padrão é `["🤔"]`. Consulte as [perguntas frequentes sobre reações do Discord](https://support.discord.com/hc/en-us/articles/12102061808663-Reactions-and-Super-Reactions-FAQ).

### `wake_prefix`

Prefixo de ativação. O padrão é `/`. Quando uma mensagem começa com `/`, o AstrBot é ativado.

> [!TIP]
> Se a sessão ativada não estiver na lista de permissões por ID, o AstrBot não responderá.

### `log_level`

Nível de log. O padrão é `INFO`. Os valores aceitos são `DEBUG`, `INFO`, `WARNING`, `ERROR` e `CRITICAL`.

### `trace_enable`

Define se o registro de rastreamentos será ativado. O padrão é `false`. Quando ativado, o AstrBot registra rastreamentos de execução, que podem ser consultados em `Data & Logs → Trace`, no painel de administração.

### `pip_install_arg`

Argumentos usados por `pip install`. Por exemplo, `-i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple`.

### `pypi_index_url`

URL do índice PyPI. O padrão é `https://mirrors.aliyun.com/pypi/simple/`.

### `persona`

*Este item de configuração está obsoleto desde a versão v4.0.0. Use a WebUI para configurar personalidades.*

Lista das personalidades configuradas. Cada personalidade contém os campos `id`, `name`, `description` e `system_prompt`.

### `timezone`

Configuração de fuso horário. Informe um nome de fuso horário da IANA, como `Asia/Shanghai`. Se estiver vazio, será usado o fuso horário padrão do sistema. Consulte a lista completa de fusos horários no [banco de dados de fusos horários da IANA](https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab).

### `callback_api_base`

Endereço base da API do AstrBot. É usado por serviços de arquivos, callbacks de plugins e outros recursos. Por exemplo, `http://example.com:6185`. O padrão é vazio, o que significa que os serviços de arquivos e os callbacks de plugins ficam desativados.

### `default_kb_collection`

Nome padrão da base de conhecimento. É usado para RAG. Se estiver vazio, nenhuma base de conhecimento será usada.

### `plugin_set`

Lista de plugins ativados. `*` significa que todos os plugins disponíveis serão ativados. O padrão é `["*"]`.
