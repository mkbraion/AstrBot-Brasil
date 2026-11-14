# Conectar ao Telegram

## Tipos de mensagem compatíveis

> Versão v4.15.0.

| Tipo de mensagem | Recebimento | Envio | Observações |
| --- | --- | --- | --- |
| Texto | Sim | Sim | |
| Imagem | Sim | Sim | |
| Mensagem de voz | Sim | Sim | |
| Vídeo | Sim | Sim | |
| Arquivo | Sim | Sim | |

**Envio proativo de mensagens:** compatível.

## 1. Criar um bot no Telegram

Primeiro, abra o Telegram e pesquise por `BotFather`. Clique em **Iniciar** e envie `/newbot`. Siga as instruções para informar o nome e o nome de usuário do bot.

Após a criação, o `BotFather` fornecerá um `token`. Guarde-o em segurança.

Se precisar usar o bot em conversas de grupo, desative o [Modo de privacidade](https://core.telegram.org/bots/features#privacy-mode) do bot. Envie o comando `/setprivacy` ao `BotFather`, selecione seu bot e escolha `Disable`.

## 2. Configurar o AstrBot

1. Acesse o painel administrativo do AstrBot.
2. Clique em **Plataformas** na barra lateral esquerda.
3. Clique em **Adicionar adaptador**, acima da lista de bots.
4. Selecione `telegram`.

Preencha os campos de configuração exibidos:

- **ID:** informe qualquer valor para diferenciar as instâncias de plataformas de mensagens.
- **Ativar:** marque esta opção.
- **Token do bot:** informe o `token` do seu bot do Telegram.

Verifique se o ambiente de rede consegue acessar o Telegram. Talvez seja necessário configurar um proxy em **Configurações → Rede → Proxy e fontes de dependências → Proxy HTTP**.

## Saída em streaming

A plataforma Telegram oferece suporte à saída em streaming. Abra **Configurações**, selecione o perfil de configuração usado pelo bot do Telegram, habilite **Saída em streaming** em **IA → Configurações comuns → Tratamento de mensagens** e clique em **Salvar configuração**.

### Streaming em conversas privadas

Em conversas privadas, o AstrBot usa a API `sendMessageDraft` (adicionada à Telegram Bot API v9.3) para gerar a saída em streaming. Ela exibe uma prévia animada de rascunho com indicador de digitação na interface da conversa, criando um efeito de digitação mais natural. Essa abordagem evita problemas do método tradicional, como cintilação da mensagem, interferência de notificações push e limites de frequência para edição de mensagens da API.

### Streaming em conversas de grupo

Em conversas de grupo, como a API `sendMessageDraft` oferece suporte apenas a conversas privadas, o AstrBot recorre automaticamente à abordagem tradicional `send_message` + `edit_message_text`.

:::warning
A API `sendMessageDraft` exige `python-telegram-bot>=22.6`.
:::
