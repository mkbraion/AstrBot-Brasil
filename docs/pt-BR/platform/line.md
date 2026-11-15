# Conectar ao LINE

## Tipos de mensagem compatíveis

> Versão v4.17.0.

| Tipo de mensagem | Receber | Enviar | Observações |
| --- | --- | --- | --- |
| Texto | Sim | Sim | |
| Imagem | Sim | Sim | |
| Áudio | Sim | Sim | |
| Vídeo | Sim | Sim | |
| Arquivo | Sim | Sim | |
| Sticker | Sim | Não | |

**Envio proativo de mensagens:** compatível.

## Criar um canal da LINE Messaging API

1. Abra o [Console de Desenvolvedores do LINE](https://developers.line.biz/console/).
2. Crie ou selecione um Provider.
3. Crie um canal do tipo `Messaging API` (não crie um canal do tipo `LINE Login`).
4. Conclua a inicialização do bot na página `Messaging API`.

## Obter as credenciais

Você precisará dos seguintes valores:

- `channel_secret`
- `channel_access_token`

Para obtê-los:

1. Abra a página de configurações do canal.
2. Na seção `Basic settings`, copie `Channel secret`.
3. Na página `Messaging API`, emita um `Channel access token`.

![](https://files.astrbot.app/docs/source/images/line/7ecee0a9102f191245330f8408eb0493.png)

## Configurar o AstrBot

1. Abra o painel de administração do AstrBot.
2. Clique em `Platforms` na barra lateral esquerda.
3. Clique em `Add Adapter`.
4. Selecione `line`.

Preencha os campos:

- `ID`: identificador personalizado para distinguir diferentes instâncias.
- `Enable`: deixe habilitado.
- `LINE Channel Access Token`: informe seu `channel_access_token`.
- `LINE Channel Secret`: informe seu `channel_secret`.
- `LINE Bot User ID`: opcional. Se ficar vazio, o AstrBot usará o valor `destination` recebido no webhook.

Clique em `Save`.

## Configurar a URL de callback (Webhook unificado)

O adaptador LINE oferece suporte **somente ao modo de Webhook unificado**.

Depois de salvar, selecione o bot em `Platforms` e clique em `View Webhook URL` para copiar a URL.

Em seguida, no Console de Desenvolvedores do LINE:

1. Abra a seção `Messaging API`.
2. Cole a URL em `Webhook settings` → `Webhook URL`.
3. Clique em `Verify`.
4. Habilite `Use webhook`.

> [!TIP]
> Se o AstrBot não estiver acessível publicamente, configure primeiro um domínio público e um proxy reverso para que o LINE consiga acessar a URL do webhook.

## Testar a integração

1. Adicione sua conta oficial do LINE como amiga.
2. Envie uma mensagem ao bot, por exemplo, `oi`.
3. Se o bot responder, a configuração foi concluída com sucesso.

Para usar o bot em um grupo, convide primeiro a conta oficial para esse grupo.
