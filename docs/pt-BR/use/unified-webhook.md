# Modo de Webhook unificado

A partir da versão v4.8.0, o AstrBot oferece suporte ao Modo de Webhook unificado (`unified_webhook_mode`). Quando esse modo está habilitado, todos os adaptadores de plataforma compatíveis utilizam o mesmo endpoint de callback do Webhook, simplificando a configuração de proxy reverso e domínio. Assim, você não precisa configurar portas, domínios e proxies reversos separados para cada adaptador de bot.

Entre os adaptadores de plataforma compatíveis com o Modo de Webhook unificado estão:

- Modo Webhook do Slack
- Conta oficial do WeChat
- Aplicativo WeCom
- Bot de IA do WeCom
- Bot de atendimento ao cliente do WeChat
- Modo Webhook do bot oficial do QQ
- ...

## Como usar o Modo de Webhook unificado

1. Tenha um domínio (por exemplo, `example.com`) e um servidor com IP público.
2. Configure a resolução DNS (por exemplo, `astrbot.example.com`).
3. Configure o proxy reverso para encaminhar as solicitações recebidas nas portas 80 ou 443 do seu domínio para a porta da WebUI do AstrBot (o padrão é 6185).
4. Acesse **Configurações → Geral → Noções básicas de execução** no AstrBot e defina **URL de callback acessível externamente** como a URL configurada (por exemplo, `https://astrbot.example.com`). Clique em salvar e aguarde a reinicialização.

Depois disso, ao configurar cada adaptador de plataforma, habilite **Modo de Webhook unificado (`unified_webhook_mode`)**.

![Configuração do Webhook unificado](https://files.astrbot.app/docs/source/images/use/unified-webhook-config.png)

Depois que esse modo for habilitado, o AstrBot gerará uma URL de callback do Webhook exclusiva para você. Basta preencher essa URL no campo de endereço de callback de cada plataforma.

![Webhook unificado](https://files.astrbot.app/docs/source/images/use/unified-webhook.png)
