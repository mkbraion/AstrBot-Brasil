# Implantar o AstrBot no 1Panel

[1Panel](https://1panel.cn/) é um painel de código aberto de nova geração para operação e gerenciamento de servidores Linux.

A equipe do 1Panel publicou o AstrBot na [loja de aplicativos do 1Panel](https://apps.fit2cloud.com/1panel), permitindo que os usuários façam a implantação e comecem a utilizá-lo diretamente pelo painel.

## Instalar o 1Panel

Se você ainda não instalou o 1Panel, consulte o [site oficial do 1Panel](https://1panel.cn/) para realizar a instalação com um único comando.

> Usuários de outros países podem consultar os tutoriais no [site oficial internacional do 1Panel](https://github.com/1Panel-dev/1Panel).

## Instalar o AstrBot

Abra o painel do 1Panel, acesse a loja de aplicativos e pesquise por `AstrBot`, conforme mostrado abaixo.

![image](https://files.astrbot.app/docs/source/images/1panel/image.png)

Clique em `Instalar` e aguarde a conclusão do processo.

Depois da instalação, abra a porta correspondente ao AstrBot (a porta padrão é 6185) na página **Sistema → Firewall** do 1Panel.

Se estiver usando um servidor em nuvem de provedores como AWS, Alibaba Cloud ou Tencent Cloud, verifique também se o grupo de segurança permite o acesso à porta 6185.

## Acessar o AstrBot

Acesse `http://IP:6185` no navegador para abrir o painel do AstrBot.
