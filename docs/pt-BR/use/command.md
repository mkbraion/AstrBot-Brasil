# Comandos integrados

Os comandos do AstrBot são registrados pelo sistema de plugins. Para manter o núcleo leve, apenas um pequeno conjunto de comandos básicos é carregado junto com o AstrBot. Outros comandos de gerenciamento e recursos avançados foram movidos para um plugin separado.

Use `/help` para consultar os comandos que estão habilitados no momento.

> [!NOTE]
> 1. `/help`, `/set` e `/unset` não aparecem por padrão na lista exibida pelo comando `/help`, mas continuam disponíveis.
> 2. Se você alterar o prefixo de ativação e remover a `/` padrão, os comandos também deverão usar o novo prefixo. Por exemplo, depois de mudar o prefixo para `!`, use `!help` e `!reset` em vez de `/help` e `/reset`.

## Comandos integrados ao núcleo

Os seguintes comandos acompanham o AstrBot e são carregados por padrão:

- `/help`: consulta os comandos habilitados no momento e as informações da versão do AstrBot.
- `/sid`: exibe informações sobre a origem da mensagem atual, incluindo UMO, ID do usuário, ID da plataforma, tipo de mensagem e ID da sessão. É útil ao configurar administradores, listas de permissões e regras de roteamento.
- `/name`: define um nome de exibição alternativo para o UMO atual — isto é, uma origem específica de mensagem de grupo ou conversa privada em uma plataforma — para facilitar sua identificação na WebUI. Exige permissão de administrador.
- `/reset`: limpa o contexto da conversa atual.
- `/stop`: interrompe as tarefas do Agent que estiverem em execução na sessão atual.
- `/new`: cria uma nova conversa e muda para ela.
- `/stats`: exibe as estatísticas de uso de tokens da conversa atual.
- `/provider`: consulta ou altera o provedor de LLM. Exige permissão de administrador.
- `/dashboard_update`: atualiza a WebUI do AstrBot. Exige permissão de administrador.
- `/set`: define uma variável de sessão, normalmente usada como variável de entrada de Agent Runners, como Dify, Coze ou DashScope.
- `/unset`: remove uma variável de sessão.

Esses comandos estão localizados em:

```text
astrbot/builtin_stars/builtin_commands
```

## Detalhes dos comandos principais

### `/sid`

`/sid` exibe informações sobre a origem da mensagem atual. Entre os principais dados retornados estão:

- `UMO`: origem unificada da mensagem atual. É usada com frequência em listas de permissões e no roteamento de configurações por sessão.
- `UID`: ID do usuário que enviou a mensagem. É usado, por exemplo, ao adicionar administradores do AstrBot.
- `Bot ID`: ID da instância da plataforma correspondente ao bot atual.
- `Message Type`: tipo de mensagem, como conversa privada ou conversa em grupo.
- `Session ID`: ID da sessão no lado da plataforma.

Em conversas em grupo, se `unique_session` estiver habilitado, `/sid` também exibe o ID do grupo. Esse ID pode ser usado para incluir o grupo inteiro em uma lista de permissões.

Usos comuns:

- **Adicionar um administrador:** execute `/sid` para obter o `UID` e, em seguida, adicione-o na WebUI em `Configuração → Controle de acesso → Administradores → IDs de administrador`.
- **Configurar listas de permissões:** selecione em `Configuração` o perfil usado pelo bot e adicione o `UMO` ou o ID do grupo em `Controle de acesso → Lista de permissões → Lista de IDs permitidos`. Isso define quais sessões podem usar o bot.
- **Configurar regras de roteamento:** use o `UMO` para diferenciar plataformas, grupos e conversas privadas.

### `/name`

`/name` define um nome de exibição legível para o UMO atual. UMO significa *Unified Message Origin* (origem unificada da mensagem). Ele identifica uma origem específica de mensagem no formato `platform ID:message type:session ID`, como um grupo do QQ, um grupo do Telegram ou uma conversa privada em determinada plataforma.

Os UMOs em seu formato original costumam ser longos e difíceis de reconhecer rapidamente. Depois que você define `/name`, o AstrBot prioriza esse nome nas listas de UMO da WebUI, nos seletores de origem de sessão, nos destinos de entrega de tarefas agendadas (cron), nos dados de conversa e em outros locais nos quais administradores precisam identificar ou selecionar uma sessão de destino. Isso reduz o risco de selecionar a origem errada ao configurar regras de roteamento, destinos de tarefas agendadas ou regras por sessão.

Quando disponível, `/name` também registra o nome automático legível fornecido pela plataforma atual, como o nome do grupo em conversas de grupo ou o apelido/ID do remetente em conversas privadas. Assim, a WebUI pode exibir um nome compreensível mesmo quando nenhum nome alternativo manual foi definido.

Uso:

- `/name <alias>`: define ou atualiza o nome alternativo do UMO atual. O comando pode ser usado várias vezes; o valor mais recente substitui o anterior.
- `/name`: sem argumento, não altera o nome alternativo. Apenas exibe as instruções de uso, o UMO atual, o nome automático atual e o nome alternativo salvo.

Regras de exibição:

- Se houver um nome alternativo e um nome automático, o AstrBot exibirá `alias (auto name)`.
- Se houver apenas o nome automático, o AstrBot exibirá esse nome.
- Se nenhum dos dois existir, o AstrBot exibirá o UMO original.

`/name` exige permissão de administrador.

### `/reset` e `/new`

Ambos os comandos interrompem as tarefas em execução na sessão atual e limpam o contexto temporário de grupo da sessão depois que a resposta é enviada. O comportamento deles em relação às conversas, porém, é diferente.

`/reset`:

- No Agent Runner integrado ao AstrBot, limpa as mensagens de contexto da conversa atual, mas preserva o ID da conversa, o título, a persona e as estatísticas de uso de tokens.
- Em Agent Runners de terceiros, como `dify`, `coze`, `dashscope` e `deerflow`, limpa o contexto do runner remoto, mas preserva o ID local da conversa.
- Se não houver uma conversa atual, retorna uma mensagem de sucesso sem criar uma conversa local.

`/new`:

- No Agent Runner integrado ao AstrBot, preserva o registro da conversa anterior, cria e seleciona uma nova conversa local e herda a persona atual.
- Em Agent Runners de terceiros, limpa primeiro o contexto do runner remoto e, em seguida, cria e seleciona uma nova conversa local. Os registros locais das conversas anteriores continuam disponíveis.

O DeerFlow também tenta excluir a thread remota anterior.

Observações sobre permissões:

- Em conversas privadas, usuários comuns podem usar os comandos por padrão.
- Em grupos, o padrão é **Seguir o isolamento da conversa (Follow Conversation Isolation)**: todos podem usar os comandos quando **Isolar conversa (Isolate Conversation)** está habilitado e a plataforma aplica o isolamento; caso contrário, somente administradores do AstrBot podem usá-los. Administradores são os IDs configurados no AstrBot, e não necessariamente os administradores do grupo detectados automaticamente. Plataformas sem suporte a isolamento mantêm a restrição de conversa compartilhada no grupo.
- Na WebUI, abra **Extensões → Manipuladores → Comando** e selecione **Mostrar comandos dos plugins do sistema (Show System Plugin Commands)**. Configure `new` e `reset` individualmente com uma destas permissões: **Todos (Everyone)**, **Somente administradores (Administrators Only)**, **Somente administradores em conversas de grupo (Administrators Only in Group Chats)** ou **Seguir o isolamento da conversa (Follow Conversation Isolation)**. A permissão selecionada vale para todos os perfis de configuração. **Seguir o isolamento da conversa** avalia o isolamento usando o perfil da mensagem recebida; as outras três opções permanecem fixas quando as configurações de isolamento são alteradas.
- **Somente administradores** restringe tanto conversas privadas quanto conversas em grupo. **Somente administradores em conversas de grupo** permite o uso por qualquer pessoa em conversas privadas, mas exige permissão de administrador em grupos.
- Com **Isolar conversa** desabilitado, o comando troca a conversa de todo o grupo; quando o isolamento está habilitado e é aplicado, afeta somente a conversa do remetente. Selecione **Todos** para permitir que membros comuns usem o comando em conversas compartilhadas do grupo.
- A desativação e a alteração do nome dos comandos também são gerenciadas nessa tela.

**Observação sobre atualização:** comandos sem permissões salvas explicitamente passam a usar **Seguir o isolamento da conversa** por padrão. As permissões salvas no gerenciamento de comandos e nas configurações de **Isolar conversa** são preservadas. Selecione **Seguir o isolamento da conversa** para restaurar as verificações automáticas de permissão. Se você personalizou os valores antigos `group_unique_on`, `group_unique_off` ou `private` em `alter_cmd.astrbot.reset`, eles não são mais lidos; selecione a permissão desejada diretamente no gerenciamento de comandos.

### `/stop`

`/stop` interrompe as tarefas do Agent que estiverem em execução na sessão atual.

Ele não limpa o histórico da conversa nem cria uma nova conversa. Apenas envia uma solicitação de interrupção às tarefas que estão sendo executadas nessa sessão.

No Agent Runner integrado, `/stop` solicita que o próprio Agent Runner interrompa a tarefa atual.  
Em Agent Runners de terceiros, como `dify`, `coze`, `dashscope` e `deerflow`, `/stop` interrompe diretamente as tarefas em execução registradas na sessão atual.

Se não houver tarefas em execução na sessão atual, o AstrBot informará que nenhuma tarefa está em execução.

### `/stats`

`/stats` exibe as estatísticas de uso de tokens da conversa atual.

O comando consulta no banco de dados todos os registros de chamadas a provedores feitos na conversa atual e exibe:

- **Total de tokens (entrada + saída):** soma dos tokens enviados ao modelo e gerados por ele.
- **Tokens de entrada (em cache):** tokens de entrada armazenados em cache pelo provedor e não cobrados novamente.
- **Tokens de entrada (outros):** tokens de entrada que não estavam em cache e foram cobrados normalmente.
- **Tokens de saída:** tokens gerados pelo modelo.

Se você não estiver em uma conversa, o AstrBot solicitará que crie uma usando `/new`.

### `/provider`

`/provider` consulta ou altera o provedor (LLM / TTS / STT) usado pelo UMO atual.

**Consultar a lista de provedores:**

Sem argumentos, `/provider` lista todos os provedores configurados, agrupados por LLM, TTS e STT. Cada provedor exibe:

- Um número de índice usado para fazer a troca.
- O ID do provedor e o modelo em uso no momento (para provedores do tipo LLM).
- O estado de conectividade: `✅` indica uma conexão saudável; `❌` indica uma falha de conexão, acompanhada de um código de erro.
- O provedor ativo é identificado pela indicação `(em uso no momento)` ao final da linha.

> [!NOTE]
> Para exibir as indicações de conectividade, habilite as verificações de disponibilidade na WebUI: selecione o perfil correspondente em `Configuração`, use o botão de pesquisa no topo para localizar `reachability_check`, habilite a opção e salve a configuração. Quando a verificação está desabilitada, os indicadores de conectividade não são exibidos e a lista é carregada mais rapidamente.

**Trocar de provedor:**

Use `/provider <index>` para trocar o provedor de LLM da sessão atual pelo provedor que ocupa o índice informado na lista.

- `/provider <index>`: troca para o provedor de LLM indicado pelo índice.
- `/provider tts <index>`: troca para o provedor de TTS indicado pelo índice.
- `/provider stt <index>`: troca para o provedor de STT indicado pelo índice.

Esse comando exige permissão de administrador.

## Extensão de comandos integrados

Outros comandos que antes acompanhavam o núcleo foram movidos para um plugin separado:

- [builtin_commands_extension](https://github.com/AstrBotDevs/builtin_commands_extension)

Esse plugin oferece comandos adicionais para gerenciamento de plugins, gerenciamento de provedores, troca de modelos, gerenciamento de personas e gerenciamento de conversas. Alguns exemplos:

- `/plugin`: consulta, habilita, desabilita ou instala plugins.
- `/op`, `/deop`: adiciona ou remove administradores.
- `/provider`: consulta ou altera provedores de LLM.
- `/model`: consulta ou altera modelos.
- `/history`: exibe o histórico da conversa atual.
- `/ls`: exibe a lista de conversas.
- `/groupnew`: cria uma nova conversa para um grupo específico.
- `/switch`: muda para uma conversa específica.
- `/rename`: renomeia a conversa atual.
- `/del`: exclui a conversa atual.
- `/persona`: consulta ou altera a persona.
- `/llm`: habilita ou desabilita a conversa com LLM.

Se precisar desses comandos adicionais, instale ou habilite o plugin `builtin_commands_extension`.

## Observações sobre permissões

Alguns comandos exigem permissão de administrador do AstrBot, como `/dashboard_update`, `/name`, `/op`, `/deop`, `/provider`, `/model` e `/persona`.

Você pode usar `/sid` para obter o ID de um usuário e, em seguida, adicioná-lo na WebUI em `Configuração → Controle de acesso → Administradores → IDs de administrador`.
