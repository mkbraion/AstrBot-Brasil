# Conectar ao Coze

O AstrBot oferece suporte à conexão com o serviço de agentes do [Coze](https://www.coze.cn/) a partir da versão v4.2.1.

## Preparação: obter uma chave de API

Primeiro, cadastre-se e entre na sua conta do [Coze](https://www.coze.cn/). Em seguida, acesse a [página de gerenciamento de chaves de API](https://www.coze.cn/open/oauth/pats) para criar uma nova chave.

Você pode seguir as etapas mostradas na imagem para chegar à página de gerenciamento ou acessar diretamente o link acima.

![Criar chave de API](https://files.astrbot.app/docs/source/images/coze/image_1.png)

Clique em **Create** (Criar). Na página seguinte, informe um nome para a chave de API, selecione o prazo de validade — tokens permanentes não são recomendados —, clique em **Select All** (Selecionar tudo) na seção **Permissions** (Permissões), escolha um espaço de trabalho e clique em **Confirm** (Confirmar).

![Criar token](https://files.astrbot.app/docs/source/images/coze/image_2.png)

Uma nova chave de API será exibida. Copie-a e guarde-a em um local seguro, pois você precisará dela mais adiante.

![Nova chave de API](https://files.astrbot.app/docs/source/images/coze/image_3.png)

## Preparação: configurar o agente

Acesse a página de [desenvolvimento de projetos](https://www.coze.cn/space/develop), clique em **+Project** no canto superior direito para criar um projeto e escolha a opção de criação de um agente.

![Criar projeto](https://files.astrbot.app/docs/source/images/coze/image_4.png)

![Criar projeto](https://files.astrbot.app/docs/source/images/coze/image_5.png)

**Importante:** depois de criar o agente, clique primeiro no botão **Publish** (Publicar), no canto superior direito. Na seção **Select Publishing Platform** (Selecionar plataforma de publicação), marque todas as opções de API e clique em **Publish**.

> Se você não publicar o agente ou não marcar as opções de API durante a publicação, não será possível chamá-lo pela API.

![Publicar agente](https://files.astrbot.app/docs/source/images/coze/image_6.png)

Depois de publicar, a criação do agente estará concluída. Na página de desenvolvimento do agente, consulte o histórico de publicações, à esquerda do botão de publicação, para confirmar que a operação foi concluída com sucesso.

Em seguida, observe o endereço da página de desenvolvimento do agente:

![Página de desenvolvimento do agente](https://files.astrbot.app/docs/source/images/coze/image_7.png)

Por exemplo, considere este endereço:

`https://www.coze.cn/space/7553214941005004863/bot/7553248674860826660`

O valor de `bot_id` corresponde à sequência numérica que aparece depois de `bot/` no endereço. No exemplo, é `7553248674860826660`.

Anote o `bot_id`; ele será necessário na configuração do AstrBot.

## Configurar o Coze no AstrBot

Depois de concluir as etapas de preparação, configure a conexão com o Coze no AstrBot.

Na WebUI, abra **Configurações**, selecione o perfil que deseja editar e acesse **IA**. Clique em **Mais ações** (`…`) ao lado do título, escolha **Alterar modo de execução** e selecione **Coze**. Leia e marque a confirmação de redefinição e clique em **Usar este modo**. Verifique se **Ativar IA** está habilitado e preencha as configurações de conexão nesta página. A troca de modo redefine a configuração do modo atual; consulte [Modo de execução de agentes](/pt-BR/use/agent-runner).

Informe a chave de API e o `bot_id` que você acabou de criar e clique em **Salvar configuração**.

> Outras observações:
>
> - **API Base URL:** normalmente, não é necessário alterar esse endereço. Se estiver usando a versão internacional do Coze, informe `https://api.coze.com`.
> - **Permitir que o Coze gerencie o histórico de conversas:** funciona conforme a descrição da própria opção.

## Salvar a configuração

Quando todos os campos estiverem preenchidos, clique em **Salvar configuração**, no canto inferior direito. Esse perfil usará diretamente o modo de execução selecionado e as configurações de conexão informadas; não é necessário selecionar separadamente um provedor de executor nem um ID de provedor.
