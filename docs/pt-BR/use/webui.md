# WebUI

O painel administrativo do AstrBot reúne gerenciamento de plugins, consulta de logs, configuração visual, estatísticas e outros recursos.

## Navegação e antigos pontos de acesso

Os caminhos abaixo correspondem à barra lateral atual, cuja ordem de menus é fixa. Os itens de extensões continuam permitindo recolher, fixar e agrupar entradas por plugin.

| Antigo ponto de acesso ou nome | Local atual |
| --- | --- |
| Providers → Add Provider → Agent Runner | Config → selecione um perfil → AI → `…` ao lado do título de AI → Change execution mode |
| Data / Dashboard | Data & Logs → Statistics |
| Conversation Management / Conversations | Data & Logs → Conversations |
| Logs / Console | Data & Logs → Logs |
| Trace | Data & Logs → Trace |
| Config → Normal Config | Config → selecione um perfil |
| Config → System Config | System Settings → General, Appearance, Network ou Security, conforme a configuração |
| Commands / Command Management | Extensions → Handlers → Command |
| Entradas independentes de MCP / Skills | Extensions → MCP Servers / Skills |
| System Settings → Appearance → Customize Sidebar | Removido; a barra lateral usa o layout padrão |
| Custom Rules / Future Tasks / SubAgents | Custom Rules fica no grupo `System` da barra lateral; Future Tasks e SubAgents ficam no grupo `Extensions` |

Os endereços antigos de logs, rastreamento, conversas e estatísticas continuam redirecionando para as abas correspondentes. Os Agent Runners agora são salvos em cada perfil; eles não são mais criados como provedores de modelos. Consulte o [Modo de execução do Agent](/en/use/agent-runner) para ver as etapas de configuração.

## Navegação da documentação

O grupo **Uso → Plugins** da documentação contém Plugins, MCP e Skills. O grupo **Uso → IA integrada do AstrBot** contém Agent Sandbox, Orquestração de SubAgents, Recursos proativos, Pesquisa na Web, Base de conhecimento e Compactação de contexto. Os endereços dessas páginas permanecem inalterados.

A ordem da barra lateral de Uso é WebUI, CLI do AstrBot, Comandos integrados, Plugins, IA integrada do AstrBot, Regras personalizadas, Modo de execução do Agent e Modo de Webhook unificado.

| Antiga entrada da documentação | Entrada atual da documentação |
| --- | --- |
| Uso → Plugins, MCP, Skills | Uso → Plugins → Guia correspondente |
| Uso → Agent Sandbox, Orquestração de SubAgents, Tarefas proativas, Pesquisa na Web, Base de conhecimento, Compactação automática de contexto | Uso → IA integrada do AstrBot → Guia correspondente |
| Uso → Uso de ferramentas / Function Calling | Removido; o guia de Pesquisa na Web explica diretamente o suporte necessário a chamadas de funções |
| Uso → Agent Runner | Uso → Modo de execução do Agent (endereço inalterado) |
| Uso → Comandos da CLI | Uso → CLI do AstrBot (endereço inalterado) |

## Acessar o painel administrativo

Depois de iniciar o AstrBot, acesse o painel administrativo pelo navegador em `http://localhost:6185`.

> [!TIP]
> - Se você implantar o AstrBot em um servidor na nuvem, substitua `localhost` pelo endereço IP do servidor.

## Login

No primeiro acesso, o AstrBot gera uma senha inicial aleatória e a exibe nos logs de inicialização. Localize a linha do log que contém as credenciais da WebUI e use essa senha para entrar. O nome de usuário normalmente é `astrbot`.

## Autenticação de dois fatores

A WebUI do AstrBot oferece autenticação de dois fatores baseada em TOTP (senha de uso único baseada em tempo).

### Habilitar a autenticação de dois fatores

1. Abra `System Settings → Security`, na parte inferior da barra lateral, e localize `WebUI Security`.
2. Ative `Enable WebUI TOTP`; será exibida uma janela de configuração com um código QR.
3. Leia o código QR com qualquer aplicativo autenticador compatível com TOTP, como o Google Authenticator.
4. Digite o código de verificação de 6 dígitos gerado pelo aplicativo para concluir a validação.
5. O sistema gerará códigos de recuperação para permitir o login caso você perca o dispositivo autenticador. Guarde-os em um local seguro.

Para substituir o segredo TOTP, use a janela de gerenciamento de TOTP. Antes, será necessário validar o código TOTP atual.

### Códigos de recuperação

- Cada código de recuperação só pode ser usado uma vez. Depois de entrar com um código de recuperação, a autenticação de dois fatores será desativada automaticamente e precisará ser configurada novamente.
- É possível gerar novos códigos de recuperação na janela de gerenciamento de TOTP.
- Se você perder os códigos de recuperação, não conseguirá recuperar o acesso à conta pelos meios normais. Será necessário editar manualmente `data/cmd_config.json`, definir `dashboard.totp.enable` como `false` e limpar manualmente `dashboard.totp.secret` e `dashboard.totp.recovery_code_hash` para desativar a autenticação de dois fatores.

### Segurança

- Depois que a autenticação de dois fatores é habilitada, alterações nas configurações relacionadas ao TOTP exigem a validação do código TOTP atual, para impedir modificações não autorizadas.
- Alterar a senha do painel administrativo revoga todos os dispositivos confiáveis.

## ChatUI

O AstrBot inclui uma ChatUI integrada para conversar diretamente, pelo navegador, com os modelos configurados.

A ChatUI oferece os seguintes fluxos de trabalho:

- A barra lateral carrega inicialmente as 30 conversas mais recentes. Role até perto do fim para carregar conversas antigas automaticamente; durante o carregamento, uma barra de progresso é exibida. As solicitações automáticas são pausadas após uma falha; selecione **Retry** para continuar. Se a lista não preencher a barra lateral, outras páginas serão carregadas automaticamente. Ao abrir uma conversa antiga pelo endereço URL, seu título e sua entrada selecionada permanecem visíveis antes de a página carregar.
- Crie, renomeie e exclua conversas, além de alternar entre conversas anteriores pela barra lateral.
- Na página de chat, selecione o perfil de configuração, o provedor de modelos e o modelo. Se a separação de sessões por provedor estiver habilitada, também será possível escolher um modelo apenas para a sessão atual.
- Envie texto, imagens, arquivos e mensagens de voz; os anexos enviados exibem prévias e passam por verificações de assinatura de arquivo para ajudar a identificar seus tipos.
- Consulte o raciocínio do modelo, o estado das chamadas de ferramentas, as referências da base de conhecimento ou da pesquisa na Web e as estatísticas de tokens e latência de cada mensagem.
- Copie respostas existentes ou gere-as novamente, inclusive usando outro modelo.
- Edite uma mensagem do usuário e continue a geração a partir daquele ponto, ou inicie uma conversa encadeada a partir de um trecho específico.
- Alterne entre os modos de resposta em streaming/normal e os modos de transporte SSE/WebSocket.

> [!NOTE]
> Para manter a ordem de entrega das mensagens, mantenha aberta apenas uma página da ChatUI para a mesma sessão do navegador. Se você abrir o chat em várias abas, o sistema poderá solicitar uma reconexão.

## Configuração visual

Selecione `Config` na barra lateral e, em seguida, escolha no seletor superior o perfil que deseja editar. As seções aparecem nesta ordem: `AI`, `Platforms & Messages`, `Access Control`, `Plugin` e `Ext.`. Use o campo de pesquisa na parte superior para localizar uma configuração. O seletor de perfil, o botão de pesquisa e a navegação entre seções permanecem fixos; somente o painel de configuração à direita rola.

- Em `AI`, as configurações da IA integrada são divididas nas abas `Model`, `Persona`, `Capabilities` e `Advanced`. Use `… → Change execution mode`, ao lado do título de AI, para conectar um agente de terceiros.
- `Access Control` contém os IDs de administradores e a lista de permissões de sessão, incluindo os logs dessa lista e as isenções de administradores.
- `Platforms & Messages` reúne as configurações de acionamento de mensagens, isolamento de sessões e entrega.
- `Plugin` permite selecionar os plugins habilitados para o perfil. Para editar os parâmetros de um plugin individual, abra `Extensions` e clique no ícone de engrenagem desse plugin (`Extension Config`).
- `Ext.` contém as configurações de resposta segmentada, contexto de conversa em grupo e texto para imagem (chave de ativação, limite de palavras, estratégia de renderização, endpoint do serviço e modelos personalizados).

| Local anterior | Local atual |
| --- | --- |
| Platform | Platforms & Messages |
| Platform → General → Administrator IDs | Access Control → Administrators → Administrator IDs |
| Platform → Whitelist | Access Control → Whitelist |

![Controle de acesso (captura da interface em inglês)](/en/use/images/config-access-control-en.jpg)

Depois de selecionar um modelo específico, clique na engrenagem ao lado do seletor para abrir a janela de configurações desse modelo. Também há engrenagens nos menus de modelos e de modelos alternativos. Clicar em uma engrenagem não altera a seleção nem a ordem dos modelos alternativos. Salvar as configurações de um modelo afeta imediatamente todos os perfis que usam esse modelo; a seleção do modelo no perfil atual ainda exige clicar em `Save Configuration`. A seleção automática não exibe uma engrenagem ao lado do seletor.

![Atalho para as configurações do modelo (captura da interface em inglês)](/en/use/images/config-model-settings-en.jpg)

Depois de editar, clique no ícone de disquete identificado como `Save Configuration`, no canto inferior direito, e confirme se a mensagem de salvamento bem-sucedido foi exibida.

Use o ícone `{}`, identificado como `Edit Configuration File`, para editar em JSON o perfil atual. Selecione `Apply This Configuration` para preparar as alterações no editor visual, feche o editor e, em seguida, selecione `Save Configuration`.

### Configurações do sistema

As configurações globais ficam em `System Settings), na parte inferior da barra lateral.

O título da página e a navegação entre seções permanecem fixos; somente o painel de configurações à direita rola.

- `General`: fuso horário, endereço de callback externo, logs e cache.
- `Appearance`: cores do tema.
- `Network`: proxy HTTP, fontes de pacotes Python e proxy do GitHub. Para saber qual endereço usar quando o AstrBot é executado no Docker, consulte [Implantar com Docker](/pt-BR/deploy/astrbot/docker).
- `Security`: HTTPS da WebUI, limites de tentativas de login e TOTP.
- `Maintenance`: backup, restauração e reinicialização.
- `OpenAPI`: chaves de acesso para desenvolvedores.

As alterações nas configurações do sistema são salvas automaticamente. Verifique se a mensagem de salvamento bem-sucedido foi exibida e reinicie o AstrBot se a página indicar que isso é necessário.

## Plugins

Selecione `Extensions` na barra lateral. As abas superiores são `Plugins`, `Skills`, `MCP Servers` e `Handlers`. Dentro de `Plugins`, alterne entre `Installed` e `AstrBot Plugin Market` para consultar os plugins locais e os disponíveis no mercado.

Em qualquer uma das listas de plugins, você também pode clicar em `Install Plugin` (+), no canto inferior direito, para instalar plugins manualmente por URL ou pelo envio de um arquivo.

> Devido ao mecanismo de atualização de plugins, a equipe do AstrBot não pode garantir integralmente a segurança dos plugins disponíveis no mercado. Verifique-os cuidadosamente. A equipe do AstrBot não se responsabiliza por perdas causadas por plugins.

### Tratar falhas no carregamento de plugins

Se um plugin não carregar, o painel administrativo exibirá a mensagem de erro e disponibilizará o botão **Reload** na lista de plugins com falha. Assim, você poderá recarregar rapidamente o plugin depois de corrigir o ambiente — por exemplo, instalando dependências ausentes — ou modificar o código, sem precisar reiniciar toda a aplicação.

## Dados e logs {#data}

Selecione `Data & Logs` na barra lateral esquerda para alternar entre `Statistics`, `Conversations`, `Logs` e `Trace`, disponíveis nas abas superiores de um mesmo espaço de trabalho. Na primeira abertura, `Statistics` é exibida por padrão; depois disso, a página volta a abrir a última aba utilizada.

### Estatísticas

A aba `Statistics` resume instâncias de plataformas, mensagens, chamadas de modelos, tokens e tempo de atividade. Ela também exibe tendências de mensagens, classificação de mensagens por plataforma, tendências de chamadas de modelos, classificação de uso de modelos e classificação de uso de modelos por conversa. Use o seletor de período na parte superior para consultar 1 dia, 3 dias ou 1 semana.

### Conversas

Use a aba `Conversations` para localizar e gerenciar registros de conversas salvos:

- Filtre por palavra-chave, ID do bot, tipo de conversa privada/em grupo ou UMO; ordene por horário de criação ou atualização.
- Por padrão, a lista carrega 30 registros por página diretamente do servidor. Quando `Group by session` está habilitado, a paginação passa a considerar sessões UMO; ao expandir uma sessão, todas as conversas dela são exibidas. O histórico completo das mensagens só é carregado depois que você seleciona uma conversa e, então, aparece na prévia à direita.
- Edite títulos, exporte várias conversas selecionadas ou exclua várias conversas selecionadas.
- Use o botão `{}` no cabeçalho da prévia para inspecionar o JSON bruto de `history` em um editor Monaco somente para leitura, com quebra automática de linha.
- Se ainda precisar da visualização original em formato de tabela, selecione `Back to legacy` no canto superior direito.

### Logs

A aba `Logs` exibe em tempo real os logs de execução do AstrBot. Você pode filtrar por nível de log e instalar pacotes Pip ausentes diretamente nessa página. Para visualizar logs DEBUG, primeiro defina `Console Log Level` como `DEBUG` em `System Settings → General → Logs`.

### Rastreamento

A aba `Trace` exibe em tempo real os rastreamentos de execução do AstrBot e é útil para depurar caminhos de chamadas de modelos e invocações de ferramentas. Use a chave na parte superior para habilitar ou desabilitar o registro de rastreamento.

> [!NOTE]
> Atualmente, o registro de rastreamento cobre apenas alguns caminhos de chamada de modelos do Agent principal do AstrBot. A cobertura será ampliada gradualmente.

## Gerenciamento de comandos

Use `Extensions → Handlers → Command` para gerenciar centralmente todos os comandos registrados; os plugins do sistema ficam ocultos por padrão.

Filtre por plugin, tipo (comando / grupo de comandos / subcomando), permissão e estado; combine esses filtros com a caixa de pesquisa para localizar itens rapidamente. As linhas de grupos de comandos podem ser expandidas para mostrar subcomandos, os indicadores exibem a quantidade de subcomandos e as linhas dos subcomandos ficam recuadas para indicar a hierarquia.

Você pode habilitar/desabilitar e renomear cada comando.

## Atualizar o painel administrativo

Quando o AstrBot é iniciado, ele verifica automaticamente se o painel administrativo precisa de atualização. Se precisar, a primeira entrada do log (em amarelo) exibirá um aviso.

Na WebUI do navegador, abra `⋮ → Update AstrBot`, no canto superior direito, expanda `Advanced settings` e clique em `Download and Update`, na opção `Update Dashboard to Latest Version Only`. Depois de uma atualização bem-sucedida, a página será atualizada automaticamente. No aplicativo para desktop, a opção de atualização abre o atualizador do próprio aplicativo.

Você também pode usar o comando `/dashboard_update` para atualizar manualmente o painel administrativo (comando de administrador).

Os arquivos do painel administrativo ficam no diretório `data/dist`. Se precisar substituí-los manualmente, baixe o arquivo `dist.zip` em https://github.com/AstrBotDevs/AstrBot/releases/ e extraia seu conteúdo no diretório `data`.

## Personalizar a porta da WebUI

Altere o valor de `port` na configuração `dashboard` do arquivo `data/cmd_config.json`.

## Esqueci a senha

Altere o valor de `password` na configuração `dashboard` do arquivo `data/cmd_config.json` e exclua todo o par chave-valor da senha.

> [!TIP]
> Para mais detalhes, consulte [Perguntas frequentes — Esqueci a senha do painel](/pt-BR/faq.md#esqueci-a-senha-do-painel).
