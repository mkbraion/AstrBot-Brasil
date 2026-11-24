# Conectar ao aplicativo Alibaba Cloud Bailian

A partir da versão v3.4.30, o AstrBot oferece suporte à conexão com aplicativos do Alibaba Cloud Bailian.

## Configurar o aplicativo Alibaba Cloud Bailian no AstrBot

No site do [Alibaba Cloud Bailian](https://bailian.console.aliyun.com/app-center#/app-center), clique para adicionar um novo aplicativo. De acordo com sua necessidade, crie um aplicativo de agente, um aplicativo de fluxo de trabalho ou um aplicativo de orquestração de agentes e configure o agente ou o fluxo de trabalho.

Anote o **ID do aplicativo**:

![ID do aplicativo](https://files.astrbot.app/docs/source/images/dashscope/image-1.png)

Entre no aplicativo, acesse **Publishing Channel → API Call → API KEY** (Canal de publicação → Chamada de API → API KEY), crie uma chave e copie o valor:

![Chave de API](https://files.astrbot.app/docs/source/images/dashscope/image-2.png)

Na WebUI do AstrBot, abra **Configurações**, selecione o perfil que deseja editar e acesse **IA**. Clique em **Mais ações** (`…`) ao lado do título, escolha **Alterar modo de execução** e selecione **Alibaba Cloud Bailian**. Leia e marque a confirmação de redefinição e clique em **Usar este modo**. Verifique se **Ativar IA** está habilitado e preencha as configurações de conexão nesta página. A troca de modo redefine a configuração do modo atual; consulte [Modo de execução de agentes](/pt-BR/use/agent-runner).

O Alibaba Cloud Bailian oferece quatro tipos de aplicativo:

- Aplicativo de agente (`agent`)
- Aplicativo de fluxo de trabalho de tarefas (`task-workflow`)
- Aplicativo de fluxo de trabalho de diálogo (`dialog-workflow`)
- Aplicativo de orquestração de agentes (`agent-arrange`)

> [!TIP]
> Conversas com várias etapas são compatíveis apenas com aplicativos de agente e aplicativos de fluxo de trabalho de diálogo. Para esses dois tipos, o AstrBot anexa automaticamente o histórico da conversa às solicitações, permitindo a continuidade do diálogo.

Verifique se o **tipo de aplicativo** (`Application Type`) configurado no AstrBot corresponde ao tipo criado no Alibaba Cloud Bailian.

Em seguida, informe o ID do aplicativo no campo **ID do aplicativo** (`Application ID`) e a chave no campo **Chave de API** (`API Key`).

Depois de preencher esses campos, clique em **Salvar configuração**.

## Salvar a configuração

Quando todos os campos estiverem preenchidos, clique em **Salvar configuração**, no canto inferior direito. Esse perfil usará diretamente o modo de execução selecionado e as configurações de conexão informadas; não é necessário selecionar separadamente um provedor de executor nem um ID de provedor.

## Apêndice: definir dinamicamente variáveis de entrada do fluxo de trabalho durante o chat (opcional)

Nos dois tipos de aplicativo de fluxo de trabalho, você pode definir variáveis de entrada dinamicamente na área de conversa.

Use o comando `/set` para definir as variáveis de entrada, conforme mostrado na imagem:

![Definir variáveis](https://files.astrbot.app/docs/source/images/dify/image-5.png)

Depois de definir as variáveis, o AstrBot anexará os valores informados à próxima solicitação enviada ao aplicativo Alibaba Cloud Bailian, permitindo adaptar o fluxo de trabalho de acordo com a necessidade.

Para cancelar uma variável definida, use o comando `/unset`. Por exemplo: `/unset name`.

As variáveis permanecem válidas durante toda a sessão atual.
