# Conectar o AstrBot à plataforma de Contas Oficiais do WeChat

O AstrBot oferece integração com a plataforma de Contas Oficiais do WeChat (versão >= v3.5.8). Após a configuração, você poderá conversar com o AstrBot diretamente pela interface de chat da Conta Oficial do WeChat.

## Antes de começar

1. Abra o Dashboard do AstrBot.
2. Clique em `Platforms` na barra lateral esquerda.
3. Clique em `Add Adapter`.
4. Selecione `weixin_official_account`.

Uma janela de configuração será exibida. Mantenha-a aberta e continue.

## Criar uma conta ou entrar na plataforma de Contas Oficiais do WeChat

Acesse a [plataforma de Contas Oficiais do WeChat](https://mp.weixin.qq.com/).

- Se você já tiver uma conta, entre nela.
- Caso contrário, registre uma nova conta e escolha `Official Account`.

> [!NOTE]
> Uma conta recém-registrada pode precisar de 1 a 2 dias para passar pela análise antes de poder ser utilizada.

## Configurar o serviço de callback

Abra `Settings & Development` → `Development Interface Management`.

![Gerenciamento da interface de desenvolvimento](https://files.astrbot.app/docs/source/images/weixin-official-account/image.png)

Copie o AppID e o AppSecret da plataforma do WeChat para os campos `appid` e `secret` do AstrBot.

Abra a lista de permissões de IP (`IP whitelist`) e adicione seu(s) IP(s) público(s), um por linha caso haja mais de um.

Na configuração do servidor, clique em modificar.

- `Token`: crie uma sequência de 3 a 32 caracteres e informe o mesmo valor no campo `token` do AstrBot.
- `EncodingAESKey`: clique em gerar aleatoriamente e informe o valor no campo `encoding_aes_key` do AstrBot.

Mantenha ativado `Unified Webhook Mode (unified_webhook_mode)` (recomendado). Clique em `Save` na janela de criação — ou em `Save changes` para um bot existente — e aguarde o recarregamento do adaptador.

Para o campo `URL`:

- Com o modo unificado ativado, copie a URL gerada em `Data & Logs → Logs` ou selecione o bot em `Platforms` e clique em `View Webhook URL`.
- Com o modo unificado desativado, use `http://<your-domain>/callback/command`.

> [!NOTE]
> O callback de Contas Oficiais do WeChat aceita somente as portas 80 ou 443. Em geral, você precisará de um domínio e de um proxy reverso:
> - Modo unificado ativado: encaminhe para a porta `6185` do AstrBot.
> - Modo unificado desativado: encaminhe para a porta `6194` do adaptador.

Defina o modo de criptografia das mensagens como `Security Mode`.

Aguarde um momento e clique em **Submit**. Se a configuração estiver correta, uma mensagem de sucesso será exibida.

## Teste

Na plataforma de Contas Oficiais do WeChat, abra o perfil da conta e localize o QR Code.

Leia-o com o WeChat, envie `help` e confira se o AstrBot responde.

Se houver resposta, a integração foi concluída com sucesso.

> [!NOTE]
> Se o console exibir `ip xxxxx not in whitelist`, significa que seu IP público ainda não está na lista de permissões do WeChat. Adicione-o e aguarde alguns minutos para que a plataforma atualize a lista.

## Proxy reverso (URL base de API personalizada)

O AstrBot aceita um endpoint personalizado por meio de `api_base_url` para ambientes sem um IP público estável.

## Entrada de áudio

Instale o `ffmpeg` para habilitar o recebimento de mensagens de áudio.

- Linux: `apt install ffmpeg`
- Windows: baixe pelo [site do FFmpeg](https://ffmpeg.org/download.html)
- macOS: `brew install ffmpeg`
