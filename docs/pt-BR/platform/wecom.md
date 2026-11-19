# Conectar o AstrBot ao WeCom

O AstrBot oferece suporte tanto a aplicativos do WeCom quanto ao atendimento ao cliente do WeCom.

## Tipos básicos de mensagem compatíveis

> Versão v4.15.0.

| Tipo de mensagem | Receber | Enviar | Observações |
| --- | --- | --- | --- |
| Texto | Sim | Sim | |
| Imagem | Sim | Sim | |
| Áudio | Sim | Sim | |
| Vídeo | Não | Sim | |
| Arquivo | Não | Sim | |

**Envio proativo de mensagens:** compatível com o aplicativo do WeCom. Ainda não foi totalmente testado no atendimento ao cliente do WeCom.

## Antes de começar

1. Abra o Dashboard do AstrBot.
2. Clique em `Platforms` na barra lateral esquerda.
3. Clique em `Add Adapter`.
4. Selecione `wecom`.

Uma janela de configuração será exibida. Mantenha-a aberta e continue com as etapas abaixo.

## Método 1: Atendimento ao cliente do WeCom

> [!NOTE]
> 1. Requer AstrBot >= v3.5.7.
> 2. Este método funciona diretamente dentro do WeChat.

1. Abra o [Console de atendimento ao cliente do WeCom](https://kf.weixin.qq.com/) e entre usando o QR Code do WeCom.
2. Crie uma conta de atendimento em `Customer Service Account` e copie o **nome** (não o ID da conta) para o campo `wechat_kf_account_name` do AstrBot.
3. Acesse as [informações da empresa no WeCom](https://work.weixin.qq.com/wework_admin/frame#profile), copie o `Corpid` e preencha o campo `corpid` do AstrBot.
4. Configure a verificação do callback:

   - Se esta for sua primeira configuração de um bot de atendimento, abra `Development Configuration` e clique em `Start` ao lado de acesso interno.
   - Se você já tiver usado esse recurso, abra diretamente `Callback Configuration` e clique em editar.

![Imagem](https://files.astrbot.app/docs/source/images/wecom/8287fd9fec5823847e6b590dc3f0f545.png)

5. Clique nos botões de geração aleatória para obter `Token` e `EncodingAESKey`. Em seguida, preencha os campos `token` e `encoding_aes_key` do AstrBot.
6. Mantenha ativado `Unified Webhook Mode (unified_webhook_mode)`, clique em `Save` e aguarde o recarregamento do adaptador.

URL de callback:

- Com o modo unificado ativado, o AstrBot gera uma URL exclusiva de callback do webhook após salvar. Copie-a em `Data & Logs → Logs` ou selecione o bot em `Platforms` e clique em `View Webhook URL`.
- Com o modo unificado desativado, use `http://<your-public-server-ip>:6195/callback/command`.

> Com o modo unificado ativado, encaminhe as solicitações externas para a porta `6185` do AstrBot. Caso contrário, encaminhe-as para a porta configurada do adaptador (padrão: `6195`).

De volta às configurações de callback do atendimento ao cliente do WeCom, clique em `Complete`. Se tudo estiver correto, o status será exibido como concluído.

7. Em `Development Configuration`, obtenha o valor de `Secret`. No AstrBot, selecione seu bot do WeCom em `Platforms`, informe esse valor em `secret`, na seção `Connection settings`, e clique em `Save changes`.

> [!TIP]
> De acordo com [#571](https://github.com/Soulter/AstrBot/issues/571), em empresas recém-registradas, o valor de `corp_id` pode levar cerca de 30 minutos para se tornar válido.

Em seguida, abra `Data & Logs` → `Logs` no AstrBot. Você deverá encontrar mensagens solicitando que abra um link de leitura de QR Code do WeChat:

```txt
Please open the following link and scan with WeChat ...
```

![Imagem](https://files.astrbot.app/docs/source/images/wecom/image-13.png)

Abra o link, leia o QR Code com o WeChat e envie `help` no chat de atendimento para testar a conexão.

## Método 2: Aplicativo do WeCom

Abra: <https://work.weixin.qq.com/wework_admin/frame#apps>

1. Clique em `My Company`, copie o ID da empresa (`Corpid`) e preencha o campo `corpid` do AstrBot.

> [!TIP]
> Em empresas recém-registradas, o valor de `corp_id` pode levar algum tempo para se tornar válido. Consulte [#571](https://github.com/Soulter/AstrBot/issues/571).

![Imagem](https://files.astrbot.app/docs/source/images/wecom/image-5.png)

2. Crie um aplicativo personalizado (`Custom App`) e preencha o nome, o avatar e o escopo de visibilidade.
3. Abra o aplicativo, copie o valor de `Secret` e preencha o campo `secret` do AstrBot.

![Imagem](https://files.astrbot.app/docs/source/images/wecom/image-4.png)

4. Nas configurações do aplicativo, localize `Receive Messages` e clique em `Set API Receive`.

![Imagem](https://files.astrbot.app/docs/source/images/wecom/image-6.png)

![Imagem](https://files.astrbot.app/docs/source/images/wecom/image-9.png)

5. Gere `Token` e `EncodingAESKey` e preencha os campos `token` e `encoding_aes_key` do AstrBot.
6. Mantenha ativado `Unified Webhook Mode (unified_webhook_mode)` (recomendado). Clique em `Save` na janela de criação — ou em `Save changes` para um bot existente — e aguarde o recarregamento do adaptador.

URL de callback:

- Com o modo unificado ativado, copie a URL gerada em `Data & Logs → Logs` ou selecione o bot em `Platforms` e clique em `View Webhook URL`.
- Com o modo unificado desativado, use `http://<your-public-server-ip>:6195/callback/command`.

> Com o modo unificado ativado, encaminhe as solicitações para a porta `6185`. Caso contrário, encaminhe-as para a porta configurada do adaptador (padrão: `6195`).

7. Configure no WeCom o IP confiável da empresa.

![Imagem](https://files.astrbot.app/docs/source/images/wecom/image-10.png)

Adicione seu IP público e confirme.

![Imagem](https://files.astrbot.app/docs/source/images/wecom/image-12.png)

Depois que o adaptador for recarregado, volte à página de recebimento da API e clique em salvar. Se aparecerem erros de verificação do callback, confira novamente todos os campos obrigatórios.

Se o salvamento for concluído, o AstrBot poderá receber mensagens do WeCom.

## Teste

No Workbench do WeCom, abra o aplicativo que você acabou de criar e envie `/help`.

Se o AstrBot responder, a integração foi concluída com sucesso.

## Proxy reverso (URL base de API personalizada)

O AstrBot aceita um endpoint personalizado do WeCom por meio de `api_base_url`, útil em ambientes sem um IP público estável.

Informe seu endpoint personalizado em `api_base_url`.

## Entrada de áudio

Instale o `ffmpeg` para habilitar o recebimento de mensagens de áudio.

- Linux: `apt install ffmpeg`
- Windows: baixe pelo [site do FFmpeg](https://ffmpeg.org/download.html)
- macOS: `brew install ffmpeg`
