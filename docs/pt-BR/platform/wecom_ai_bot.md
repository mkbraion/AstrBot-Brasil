# Conectar à plataforma de Bot de IA do WeCom

O Bot de IA do WeCom é uma plataforma oficial de bots com suporte a IA oferecida pelo WeCom. Ele pode ser usado diretamente em conversas individuais e em grupos internos, além de oferecer suporte a respostas em streaming.

O AstrBot oferece suporte a essa plataforma desde a versão v4.3.5.

## Tipos básicos de mensagem compatíveis

| Tipo de mensagem | Receber | Enviar | Observações |
| --- | --- | --- | --- |
| Texto | Sim | Sim | |
| Imagem | Sim | Sim | Requer a configuração da URL de webhook para envio de mensagens. |
| Áudio | Não | Sim | Requer a configuração da URL de webhook para envio de mensagens. |
| Vídeo | Não | Sim | Requer a configuração da URL de webhook para envio de mensagens. |
| Arquivo | Não | Sim | Requer a configuração da URL de webhook para envio de mensagens. |

**Envio proativo de mensagens:** compatível, mas requer uma URL de webhook para envio de mensagens.

## Configurar o Bot de IA do WeCom

1. Entre no [Console de administração do WeCom](https://work.weixin.qq.com/wework_admin).
2. Na barra lateral esquerda, abra `Management Tools` → `AI Bot` e clique em **Create Bot**.

![Ferramentas de gerenciamento — Bot de IA](https://files.astrbot.app/docs/source/images/wecom_ai_bot/image-1.png)

3. Na página de criação, escolha `Create via API Mode`. Preencha o nome do bot, o avatar e as demais informações básicas.

   Gere `Token` e `EncodingAESKey` usando a geração aleatória, mas ainda não clique em **Create**.

![Criar conta do Bot de IA](https://files.astrbot.app/docs/source/images/wecom_ai_bot/image.png)

## Configurar o AstrBot

1. Abra o Dashboard do AstrBot, clique em `Platforms`, depois em `+ Add Adapter` e selecione `WeCom AI Bot`.

2. Preencha os campos do AstrBot com os valores da página de criação do Bot de IA do WeCom:

   - Nome do bot
   - `token`
   - `encoding_aes_key`
   - `id` (qualquer valor exclusivo)
   - `port` (padrão: `6198`; altere se necessário)

   Mantenha ativado `Unified Webhook Mode (unified_webhook_mode)` e clique em **Save**.

3. Volte à página de criação do Bot de IA do WeCom e configure o campo `URL`:

   - Com o modo unificado ativado, o AstrBot gera uma URL exclusiva de callback após salvar. Copie-a em `Data & Logs → Logs` ou selecione o bot em `Platforms` e clique em `View Webhook URL`.
   - Com o modo unificado desativado, use `http://IP:port/webhook/wecom-ai-bot`.

> Recomendamos usar um domínio com proxy reverso e HTTPS. Você também pode usar o [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/tunnel-guide/).

4. Clique em **Create**. Se tudo der certo, você será direcionado à página de detalhes do bot.

   Se aparecer a mensagem `Service did not respond correctly`, confira novamente a configuração do AstrBot e as regras do firewall.

![Detalhes do bot](https://files.astrbot.app/docs/source/images/wecom_ai_bot/image-3.png)

5. Opcional (recomendado): configure a URL de webhook para envio de mensagens do WeCom.

   Por padrão, o Bot de IA do WeCom só responde depois que os usuários enviam uma mensagem. A configuração do webhook de envio permite receber notificações proativas.

6. Opcional (recomendado): habilite `Send messages via Webhook only` para obter saídas com várias mensagens e contornar o limite de uma única bolha de resposta.

   Essa opção requer a URL de webhook para envio de mensagens configurada na etapa 5.

## Usar o bot

### Adicionar o bot a um grupo

No cliente do WeCom, abra um grupo interno, clique em **Add Member** → **AI Bot**, selecione o bot criado e adicione-o ao grupo.

![Adicionar membro](https://files.astrbot.app/docs/source/images/wecom_ai_bot/image-4.png)

![Adicionado com sucesso](https://files.astrbot.app/docs/source/images/wecom_ai_bot/image-5.png)

### Conversar com o bot

Envie uma mensagem em uma conversa privada ou em um grupo para falar com o bot.

Se quiser um efeito de resposta em streaming, semelhante à digitação, habilite **Streaming Reply** no AstrBot.

![Resposta em streaming](https://files.astrbot.app/docs/source/images/wecom_ai_bot/image-6.png)

## Ajuda e suporte

Se tiver problemas durante a configuração ou o uso, ou precisar de suporte empresarial, entre em contato: [community@astrbot.app](mailto:community@astrbot.app).
