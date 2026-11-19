# Conectar uma conta pessoal do WeChat

> Introduzido na versão v4.22.0.

O AstrBot oferece suporte à conexão de uma conta pessoal do WeChat por meio do adaptador `Personal WeChat`. Esse adaptador é implementado sobre a interface oficial `openclaw-weixin` da Tencent, usa login por QR Code com *long polling* e não exige uma URL de callback de Webhook.

> [!NOTE]
> Atualize o aplicativo móvel do WeChat para uma versão recente.
>
> **iOS**: >= 4.0.70

## Tipos de mensagem compatíveis

| Tipo de mensagem | Receber | Enviar | Observações |
| --- | --- | --- | --- |
| Texto | Sim | Sim | |
| Imagem | Sim | Sim | No recebimento, o arquivo é baixado e descriptografado no diretório temporário local |
| Áudio | Sim* | Não | *É usada a transcrição feita na nuvem do WeChat; não é necessária transcrição local |
| Vídeo | Sim | Sim | No recebimento, o arquivo é baixado e descriptografado no diretório temporário local |
| Arquivo | Sim | Sim | No recebimento, o arquivo é baixado e descriptografado no diretório temporário local |

## Criar o bot

1. Abra a WebUI do AstrBot.
2. Clique em `Platforms` na barra lateral esquerda.
3. Clique em `Add Adapter`, acima da lista de bots.
4. Selecione `Personal WeChat`.
5. O QR Code de login será exibido diretamente. Leia-o com o WeChat no celular e confirme o login no próprio WeChat.
6. Depois que o login for concluído, clique em **Save**.

## Observações sobre a configuração

Na maioria dos casos, basta prestar atenção aos seguintes campos:

- `ID(id)`: qualquer valor de sua preferência, usado para distinguir diferentes instâncias de bot.
- `Enable(enable)`: habilite esta opção.

Mantenha as demais opções com os valores padrão, a menos que saiba exatamente por que precisa alterá-las:

- `QR Poll Interval (weixin_oc_qr_poll_interval)`
- `Long Poll Timeout (weixin_oc_long_poll_timeout_ms)`
- `API Timeout (weixin_oc_api_timeout_ms)`

> [!TIP]
> Os campos `token` e `account_id` são salvos automaticamente pelo AstrBot depois que o login por QR Code é concluído. Normalmente, você não precisa preenchê-los manualmente.

## Login por QR Code

Depois que você selecionar `Personal WeChat`, o AstrBot solicitará automaticamente um QR Code de login ao WeChat e o exibirá na janela de criação do bot. Leia o código com o WeChat no celular e confirme o login. Quando a área do QR Code indicar que o login foi bem-sucedido, clique em **Save** para concluir a criação do bot.

Depois que o login for concluído e o bot for salvo, o AstrBot armazenará automaticamente o estado da sessão. Nas próximas reinicializações, se a sessão ainda estiver válida, normalmente não será necessário ler o QR Code novamente.

> [!NOTE]
> Se o QR Code expirar, feche e abra novamente a janela de criação do bot ou selecione `Personal WeChat` outra vez para solicitar um novo código.

## Verificação

Depois que o login for concluído, envie uma mensagem pelo WeChat. Se o AstrBot responder normalmente, a integração está funcionando.

Você também pode acompanhar `Data & Logs` → `Logs` na WebUI para confirmar que o adaptador concluiu o login e começou a consultar as mensagens periodicamente.

## Armazenamento de arquivos de mídia

Imagens, vídeos, arquivos e mensagens de áudio recebidos são baixados e descriptografados no diretório temporário local do AstrBot:

`data/temp`

Esses arquivos são armazenados temporariamente em cache e podem ser utilizados posteriormente por plugins, agentes ou pelo serviço de arquivos.

## Observações

- Este adaptador realiza o login por meio da leitura de um QR Code com uma conta pessoal do WeChat. Portanto, o processo de configuração é diferente daquele usado para Contas Oficiais do WeChat e WeCom.
- Não é necessária uma URL pública de callback, e o modo de Webhook unificado não precisa ser habilitado.
