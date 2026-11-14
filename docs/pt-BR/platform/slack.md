# Conectar ao Slack

## Criar o adaptador da plataforma Slack no AstrBot

Acesse a página **Plataformas**, clique em **Adicionar adaptador**, localize o Slack e clique nele para abrir a página de configuração.

![Selecionar a plataforma de mensagens Slack](/slack/image-1.png?v=2)

## Criar um aplicativo no Slack

O Slack oferece dois métodos de conexão: `Webhook` e `Socket`. Se você não tiver um servidor público e o volume de mensagens for relativamente baixo, recomendamos o método `Socket`. Se você tiver um servidor público (ou conhecimento técnico para configurar túneis, como o Cloudflare Tunnel), poderá escolher o método `Webhook`. Em geral, o método `Socket` é mais simples de implantar.

1. Crie uma conta no [Slack](https://slack.com/signin) e um espaço de trabalho (*Workspace*).
2. Acesse [Gerenciamento de aplicativos](https://api.slack.com/apps), clique em **Create New App** → **Blank app** → **Continue**. Informe o **App Name**, selecione o espaço de trabalho ao qual deseja adicioná-lo e clique em **Create**.
3. (Somente para `Webhook`) Obtenha o `Signing Secret`. Na página **Basic Information**, na barra lateral esquerda, localize **Signing Secret** em **App Credentials**, clique em **Show**, copie o valor e cole-o no campo `signing_secret` da configuração do adaptador de plataforma.

![Signing Secret](https://files.astrbot.app/docs/source/images/slack/image.png)

4. Na página **Basic Information**, na barra lateral esquerda, localize **App-Level Tokens** e clique em **Generate Token and Scopes**. Informe qualquer nome para o token, clique em **Add Scope**, selecione `connections:write` e clique em **Generate**. Clique em **Copy** e cole o resultado no campo `app_token` da página de configuração do AstrBot.

![Gerar token e escopos](https://files.astrbot.app/docs/source/images/slack/image-2.png)

5. Na página **OAuth & Permissions**, na barra lateral esquerda, adicione as permissões a seguir em **Bot Token Scopes**:

   - `channels:history`
   - `channels:read`
   - `channels:write.invites`
   - `chat:write`
   - `chat:write.customize`
   - `chat:write.public`
   - `files:read`
   - `files:write`
   - `groups:history`
   - `groups:read`
   - `groups:write`
   - `im:history`
   - `im:read`
   - `im:write`
   - `mpim:read`
   - `reactions:read`
   - `reactions:write`
   - `users:read`

   Ao assinar o evento `member_joined_channel`, o Slack exige automaticamente o escopo `mpim:read` para consultar informações básicas das mensagens diretas em grupo das quais o bot participa.

6. Na página **OAuth & Permissions**, na barra lateral esquerda, clique em **Install to xxx**, na seção **OAuth Token** (em que `xxx` é o nome do seu espaço de trabalho). Em seguida, copie o **Bot User OAuth Token** gerado para o campo `bot_token` da configuração do adaptador.

7. (Somente para `Socket`) Na página **Socket Mode**, na barra lateral esquerda, habilite o **Socket Mode**.

![Habilitar o Socket Mode](https://files.astrbot.app/docs/source/images/slack/image-3.png)

## Iniciar o adaptador da plataforma

A configuração está concluída. Se estiver usando o modo `Socket`, basta clicar em **Salvar** no canto inferior direito da configuração.

Se estiver usando o modo `Webhook`, mantenha habilitada a opção **Unified Webhook Mode (`unified_webhook_mode`)**.

> [!TIP]
> Antes da versão v4.8.0, o **Unified Webhook Mode** não existia. Nesse caso, era necessário preencher os seguintes campos de configuração:
> **Slack Webhook Host**, **Slack Webhook Port** e **Slack Webhook Path**.

## Habilitar assinaturas de eventos

Depois de criar o adaptador da plataforma, volte às configurações do Slack. Na página **Event Subscriptions**, na barra lateral esquerda, clique em **Enable Events** para habilitar o recebimento de eventos.

Se estiver usando o modo `Webhook`:

- Com o **Unified Webhook Mode** habilitado, depois de salvar, o AstrBot gera automaticamente uma URL exclusiva de callback do Webhook. Você pode encontrá-la em **Dados e registros → Registros** ou selecionar o bot em **Plataformas** e clicar em **Ver URL do Webhook**. Informe essa URL no campo **Request URL**.
- Com o **Unified Webhook Mode** desabilitado, informe `https://your-domain/astrbot-slack-webhook/callback` no campo **Request URL**.

> [!TIP]
> No modo `Webhook`, primeiro configure seu domínio no provedor de DNS. Em seguida, use um software de proxy reverso para encaminhar as solicitações à porta `6185` do servidor AstrBot (quando o Unified Webhook Mode estiver habilitado) ou à porta definida na configuração (quando estiver desabilitado). Como alternativa, você pode usar o Cloudflare Tunnel. Há tutoriais detalhados disponíveis na Internet; este guia não abordará esses procedimentos.

Depois de habilitar os eventos, na seção **Subscribe to bot events**, clique em **Add Bot User Event** e adicione os seguintes eventos:

1. `channel_created`
2. `channel_deleted`
3. `channel_left`
4. `member_joined_channel`
5. `member_left_channel`
6. `message.channels`
7. `message.groups`
8. `message.im`
9. `reaction_added`
10. `reaction_removed`
11. `team_join`

Depois de adicionar os eventos, clique em **Save Changes**, na parte inferior da página, para salvar as assinaturas antes de realizar o teste abaixo.

## Testar a conexão

Acesse o espaço de trabalho do Slack que você acabou de adicionar e abra o canal em que deseja usar o bot. Em seguida, mencione o aplicativo que acabou de criar com `@`. Na mensagem enviada pelo Slackbot, clique em **Add** para adicioná-lo ao espaço de trabalho. Depois, mencione o aplicativo e digite `/help`. Se ele responder corretamente, o teste foi bem-sucedido.

Se tiver dúvidas, [abra uma Issue](https://github.com/AstrBotDevs/AstrBot/issues).
