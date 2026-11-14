# Conectar ao Discord

## Criar o adaptador da plataforma Discord no AstrBot

Abra **Plataformas** na WebUI, clique em **Adicionar adaptador** e selecione **Discord**. Preencha as configurações a seguir e clique em **Salvar** depois de obter o token.

- **Nome do bot:** personalize o nome para distinguir facilmente os diferentes adaptadores.
- **Ativar:** marque esta opção para habilitar o adaptador.
- **Token do bot:** token obtido após criar um aplicativo no Discord (veja as instruções abaixo).
- **Endereço de proxy do Discord:** se precisar de um proxy para acessar o Discord, informe o endereço aqui (opcional).
- **Registrar automaticamente comandos de plugins como comandos de barra do Discord:** quando habilitada, esta opção registra automaticamente os comandos dos plugins instalados como comandos de barra (*slash commands*) do Discord, facilitando o uso.

## Criar um aplicativo no Discord

1. Acesse o [Portal do desenvolvedor do Discord](https://discord.com/developers/applications), clique no botão azul no canto superior direito, informe o nome do aplicativo e crie-o.

![Criar bot (informar o nome)](https://files.astrbot.app/docs/source/images/discord/image-1.png)

2. Clique em **Bot** na barra lateral esquerda e, em seguida, no botão **Reset Token**. Depois que o token for criado, clique em **Copy** e cole-o no campo **Token do bot do Discord** da configuração.

![Opções do token](https://files.astrbot.app/docs/source/images/discord/image-4.png)

3. Role a página para baixo e habilite as três opções a seguir:

![Captura das opções Presence Intent, Server Members Intent e Message Content Intent](https://files.astrbot.app/docs/source/images/discord/image-2.png)

- **Presence Intent:** permite que o bot acesse o status de presença dos usuários.
- **Server Members Intent:** permite que o bot acesse informações dos membros do servidor.
- **Message Content Intent:** permite que o bot leia o conteúdo das mensagens.

4. Clique em **OAuth2** na barra lateral esquerda e, no **OAuth2 URL Generator**, selecione `Bot`.

   Exemplo:

   ![Gerador de URL OAuth2](https://files.astrbot.app/docs/source/images/discord/image-6.png)

   Na seção **Bot Permissions**, exibida logo abaixo, selecione as permissões necessárias. Em geral, recomenda-se habilitar:

   - `Send Messages`
   - `Create Public Threads`
   - `Create Private Threads`
   - `Send TTS Messages`
   - `Manage Messages`
   - `Manage Threads`
   - `Embed Links`
   - `Attach Files`
   - `Read Message History`
   - `Add Reactions`

   Se preferir, você pode conceder diretamente a permissão `Administrator`. Ainda assim, em produção, recomendamos usar somente as permissões listadas acima (ou as permissões específicas de que você realmente precisa).

> Lembre-se: quanto maiores forem as permissões concedidas, maior será o risco.

5. Copie a URL gerada exibida abaixo. Abra essa URL para adicionar o bot ao servidor desejado.

![Localização da URL gerada](https://files.astrbot.app/docs/source/images/discord/image-5.png)

6. Acesse o servidor do Discord. Seu bot deverá aparecer como conectado.

![Bot conectado](https://files.astrbot.app/docs/source/images/discord/image-7.png)

Mencione o bot que você acabou de criar (ou envie a mensagem sem mencioná-lo) e digite `/help`. Se ele responder corretamente, o teste foi bem-sucedido.

## Emoji de pré-confirmação

O Discord oferece o recurso de emoji de pré-confirmação. Quando habilitado, o bot adiciona uma reação com emoji enquanto processa uma mensagem, indicando aos usuários que está trabalhando na solicitação.

Abra **Configurações**, selecione o perfil de configuração usado pelo bot, clique no botão de pesquisa e procure por `platform_specific.discord.pre_ack_emoji`. Depois de editar, clique em **Salvar configuração**:

- **Ativar emoji de pré-confirmação:** quando habilitada, esta opção faz o bot adicionar automaticamente uma reação com emoji ao receber uma mensagem.
- **Lista de emojis:** informe símbolos de emoji Unicode, por exemplo, 👍, 🤔, ⏳. Você pode adicionar vários emojis; o bot escolherá um deles aleatoriamente para usar.

# Solução de problemas

- Se você chegar à etapa final e o bot não ficar online, verifique se o servidor consegue se conectar diretamente ao Discord.

Se tiver dúvidas, [abra uma Issue](https://github.com/AstrBotDevs/AstrBot/issues).
