# Implantar o AstrBot no BT Panel

O [BT Panel](https://www.bt.cn/new/index.html) é um painel de gerenciamento de servidores Linux e Windows, desenvolvido para oferecer segurança, eficiência e recursos prontos para produção.

O AstrBot está disponível na loja de aplicativos Docker do BT Panel, com suporte à instalação em um clique.

## Instalar o BT Panel

Se você ainda não instalou o BT Panel, consulte a página [Instalar produtos BT](https://www.bt.cn/new/download.html) para fazer a instalação.

## Configurar a URL de aceleração (usuários da China continental)

Depois de abrir o BT Panel, clique em `Docker` na barra lateral, acesse as configurações e altere o campo `Acceleration URL`.

![alt text](https://files.astrbot.app/docs/source/images/btpanel/image-1.png)

## Instalar o AstrBot

Acesse a loja de aplicativos do Docker e pesquise por `AstrBot`, conforme mostrado abaixo.

![image](https://files.astrbot.app/docs/source/images/btpanel/image.png)

Clique em **Instalar** e aguarde a conclusão do processo.

Depois da instalação, clique em `Security` na barra lateral e libere a porta correspondente ao AstrBot (a porta padrão é 6185).

Se estiver usando um servidor em nuvem de provedores como AWS, Alibaba Cloud ou Tencent Cloud, verifique também se o grupo de segurança permite o acesso à porta correspondente.

## Acessar o AstrBot

Acesse `http://IP:6185` no navegador para abrir o painel do AstrBot.

> [!TIP]
> Por padrão, o procedimento acima libera somente a porta 6185. Se você também quiser integrar plataformas de mensagens, será necessário liberar as portas correspondentes.
>
> Clique em `Container` na barra superior, localize o contêiner do AstrBot, clique em `Manage`, depois em `Edit Container` e adicione as portas necessárias.
>
> ![image](https://files.astrbot.app/docs/source/images/btpanel/image-2.png)
>
> Consulte a tabela abaixo para conhecer algumas portas usadas pelas integrações:
>
> | Porta | Descrição | Tipo |
> | --- | --- | --- |
> | 6185 | Porta padrão da WebUI do AstrBot | Obrigatória |
> | 6195 | Porta padrão do WeCom | Opcional |
> | 6199 | Porta padrão da conta pessoal do QQ (aiocqhttp) | Opcional |
> | 6196 | Porta padrão da API oficial do QQ (Webhook) | Opcional |
>
> As plataformas que não aparecem na tabela não exigem a abertura de portas adicionais.
