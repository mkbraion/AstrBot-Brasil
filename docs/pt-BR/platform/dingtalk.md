# Conectar ao DingTalk

## Tipos básicos de mensagem compatíveis

> Versão v4.15.0.

| Tipo de mensagem | Receber | Enviar | Observações |
| --- | --- | --- | --- |
| Texto | Sim | Sim | |
| Imagem | Sim | Sim | |
| Voz | Não | Sim | |
| Vídeo | Não | Sim | |
| Arquivo | Não | Sim | |

**Envio proativo de mensagens:** compatível.

## Criar e configurar o aplicativo

O DingTalk oferece dois métodos de configuração: criação por QR Code com um clique no AstrBot ou criação manual de um aplicativo na Plataforma Aberta do DingTalk.

### Opção 1: criação por QR Code com um clique

Requisito de versão do AstrBot: >= v4.25.0.

Abra o Dashboard do AstrBot -> `Platforms` -> `Add Adapter` e selecione `DingTalk`.

Em `Creation Method`, selecione `One-click QR setup`. Leia o QR Code com o aplicativo móvel do DingTalk e, na página de autorização da plataforma, crie um bot ou vincule um bot existente. Quando a criação for concluída, o AstrBot preencherá automaticamente `ClientID` e `ClientSecret`. Clique em `Save` para finalizar.

Depois de concluir a criação pelo QR Code, continue com as etapas abaixo para conferir a assinatura de eventos, publicar uma versão e adicionar o bot a um grupo.

### Opção 2: criação manual

Acesse a [Plataforma Aberta do DingTalk](https://open-dev.dingtalk.com/fe/app) e crie um aplicativo:

![Criar um aplicativo](https://files.astrbot.app/docs/source/images/dingtalk/image-4.png)

Depois de criar o aplicativo, adicione uma capacidade e escolha **Bot**:

![Adicionar a capacidade Bot](https://files.astrbot.app/docs/source/images/dingtalk/image-5.png)

Abra as configurações do bot e preencha as informações:

![Configurações do bot](https://files.astrbot.app/docs/source/images/dingtalk/image-7.png)

Depois de conferir todas as configurações, clique em **Publish**.

Acesse **Credentials & Basic Information** e copie `ClientID` e `ClientSecret`.

## Conectar ao AstrBot

Abra o Dashboard do AstrBot -> `Platforms` -> `Add Adapter` e crie um adaptador DingTalk.

Se quiser que o AstrBot crie o aplicativo, selecione `One-click QR setup` e conclua a leitura do código. Se você já criou o aplicativo manualmente, selecione `Manual setup`, preencha `ClientID` e `ClientSecret` e clique em `Save`. O AstrBot solicitará automaticamente a autorização à Plataforma Aberta do DingTalk.

Volte à Plataforma Aberta do DingTalk, abra **Event Subscriptions**, selecione `Stream mode push` e clique em `Save`. Se tudo estiver correto, o status indicará que a conexão foi estabelecida.

![Assinatura de eventos](https://files.astrbot.app/docs/source/images/dingtalk/image-8.png)

Salve a configuração.

## Publicar uma versão

Na barra lateral esquerda, abra **Version Management and Release** e crie uma nova versão.

Preencha o número da versão, a descrição e o escopo de visibilidade (todos os funcionários ou o público necessário). Em seguida, salve e publique.

![Publicar uma versão](https://files.astrbot.app/docs/source/images/dingtalk/image-11.png)

Abra uma conversa em grupo no DingTalk e clique nas configurações, no canto superior direito:

![Configurações do grupo](https://files.astrbot.app/docs/source/images/dingtalk/image-12.png)

Role a página até **Add Bot**, selecione o bot que você acabou de criar e adicione-o:

![Adicionar o bot ao grupo](https://files.astrbot.app/docs/source/images/dingtalk/image-9.png)

## Concluído

Em uma conversa de grupo, mencione o bot e envie `/help`. Se ele responder, a integração foi concluída com sucesso.
