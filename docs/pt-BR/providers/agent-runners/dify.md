# Conectar ao Dify

## Instalar o Dify

Se você ainda não instalou o Dify, consulte a [documentação de instalação do Dify](https://docs.dify.ai/getting-started/install-self-hosted) para realizar a instalação.

## Configurar o Dify no AstrBot

Na WebUI, abra **Configurações**, selecione o perfil que deseja editar e acesse **IA**. Clique em **Mais ações** (`…`) ao lado do título, escolha **Alterar modo de execução** e selecione **Dify**. Leia e marque a confirmação de redefinição e clique em **Usar este modo**. Verifique se **Ativar IA** está habilitado e preencha as configurações de conexão nesta página. A troca de modo redefine a configuração do modo atual; consulte [Modo de execução de agentes](/pt-BR/use/agent-runner).

No Dify, cada `API Key` corresponde exclusivamente a um aplicativo. Portanto, você pode configurar chaves de API diferentes em perfis separados para conectar vários aplicativos Dify.

O AstrBot oferece as seguintes opções de **tipo de aplicativo** (`Application Type`):

- `chat`
- `chatflow`
- `agent`
- `workflow`

> [!TIP]
> Verifique se o tipo de aplicativo definido no AstrBot corresponde ao tipo criado no Dify.
>
> ![Tipos de aplicativo](https://files.astrbot.app/docs/source/images/dify/image-3.png)

### Aplicativos de chat e de agente

Crie as chaves de API dos aplicativos de chat e de agente do Dify conforme mostrado nas imagens:

![Chave de API para chat e agente](https://files.astrbot.app/docs/source/images/dify/chat-agent-api-key.png)

![Segunda etapa da chave de API para chat e agente](https://files.astrbot.app/docs/source/images/dify/chat-agent-api-key-2.png)

Copie a chave e cole-a no campo `API Key` da configuração. Em seguida, clique em **Salvar configuração**.

### Aplicativos de fluxo de trabalho

#### Configurar os nomes das variáveis de entrada e saída

Os aplicativos de fluxo de trabalho recebem variáveis de entrada, executam o fluxo e retornam os resultados.

![Variáveis de entrada e saída do fluxo de trabalho](https://files.astrbot.app/docs/source/images/dify/workflow-io-key.png)

Em cada solicitação para aplicativos do tipo `workflow`, o AstrBot anexa duas variáveis:

- `astrbot_text_query`: nome da variável de entrada que contém o texto informado pelo usuário.
- `astrbot_session_id`: ID da sessão.

Você pode personalizar o nome da variável de entrada na configuração, no campo **Prompt Input Variable** (Variável de entrada do prompt) das opções do Dify.

É necessário ajustar o nome da variável de entrada do fluxo de trabalho para que corresponda ao valor configurado no AstrBot.

Ao final, o fluxo de trabalho retorna um resultado. Você pode personalizar o nome da variável que contém esse resultado no campo **Workflow Output Variable** (Variável de saída do fluxo de trabalho) das opções do Dify. O valor padrão é `astrbot_wf_output`. Configure esse mesmo nome no nó de saída do fluxo de trabalho do Dify; caso contrário, o AstrBot não conseguirá interpretar o resultado corretamente.

#### Criar uma chave de API

Crie a chave de API do aplicativo de fluxo de trabalho do Dify conforme mostrado na imagem.

Clique no botão **Publish** (Publicar), no canto superior direito, acesse **Access API** (Acessar API), clique em **API Key** no canto superior direito e selecione **Create Key** (Criar chave). Em seguida, copie a chave de API.

![Chave de API do fluxo de trabalho](https://files.astrbot.app/docs/source/images/dify/workflow-api-key.png)

Copie a chave e cole-a no campo `API Key` da configuração. Em seguida, clique em **Salvar configuração**.

## Salvar a configuração

Quando todos os campos estiverem preenchidos, clique em **Salvar configuração**, no canto inferior direito. Esse perfil usará diretamente o modo de execução selecionado e as configurações de conexão informadas; não é necessário selecionar separadamente um provedor de executor nem um ID de provedor.

## Apêndice: definir dinamicamente variáveis de entrada do fluxo de trabalho durante o chat (opcional)

Você pode usar o comando `/set` para definir variáveis de entrada dinamicamente, conforme mostrado na imagem:

![Definir variáveis](https://files.astrbot.app/docs/source/images/dify/image-5.png)

Depois de definir as variáveis, o AstrBot anexará os valores informados à próxima solicitação enviada ao Dify, permitindo adaptar o fluxo de trabalho.

![Variáveis definidas](https://files.astrbot.app/docs/source/images/dify/image-4.png)

Para cancelar as variáveis definidas, use o comando `/unset`.

As variáveis permanecem válidas durante toda a sessão atual.
