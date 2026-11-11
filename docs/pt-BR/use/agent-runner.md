# Modo de execução de agentes {#agent-runner}

O Agent Runner é um componente do AstrBot responsável por executar agentes.

A partir da versão v4.7.0, três provedores — Dify, Coze e Aplicativo Alibaba Cloud Bailian — foram migrados para a camada Agent Runner, reduzindo conflitos com os recursos existentes do AstrBot. Se você atualizar de uma versão anterior para a v4.7.0, não precisa fazer nada: o AstrBot realiza a migração automaticamente. Versões posteriores também adicionaram suporte ao DeerFlow como provedor de Agent Runner.

Atualmente, o AstrBot oferece suporte a cinco Agent Runners:

- Agent Runner integrado do AstrBot
- Agent Runner do Dify
- Agent Runner do Coze
- Agent Runner do Aplicativo Alibaba Cloud Bailian
- Agent Runner do DeerFlow

Por padrão, o Agent Runner integrado do AstrBot é o executor utilizado.

## Por que separar o Agent Runner

Nas versões anteriores, plataformas com recursos de agente integrados, como Dify, Coze e Aplicativo Alibaba Cloud Bailian, eram integradas ao AstrBot como provedores de chat comuns. Na prática, percebemos que elas são fundamentalmente diferentes dos provedores de chat tradicionais, que apenas realizam a conclusão de texto. Forçá-las a compartilhar a mesma camada causava conflitos de projeto e de uso. Por isso, a partir da versão v4.7.0, elas passaram a ser abstraídas em Agent Runners independentes.

Do ponto de vista da arquitetura, a diferença pode ser entendida assim:

- O provedor de chat é responsável por **conversar**;
- O Agent Runner é responsável por **pensar e agir**.

O Agent Runner chama a interface do provedor de chat e, com base na resposta recebida, executa ciclos de várias etapas: perceber → planejar → executar uma ação → observar o resultado → planejar novamente.

Um provedor de chat é essencialmente uma interface de conclusão de turno único: recebe como entrada o prompt, o histórico da conversa e a lista de ferramentas, e produz respostas do modelo, como texto e instruções de chamada de ferramentas.

Um Agent Runner normalmente funciona como um ciclo (*loop*): recebe a intenção do usuário, o contexto e o estado do ambiente; elabora um plano com base em uma estratégia ou modelo (*Plan*); seleciona e chama ferramentas (*Act*); lê os resultados do ambiente (*Observe*); interpreta novamente esses resultados, atualiza o estado interno, decide a próxima ação e repete o processo até concluir a tarefa ou atingir o tempo limite.

![Arquitetura do Agent Runner](https://files.astrbot.app/docs/source/images/use/agent-runner/agent-arch.svg)

Plataformas como Dify, Coze, Aplicativo Bailian e DeerFlow já possuem esse ciclo integrado. Se forem tratadas como provedores de chat comuns, haverá conflito com a funcionalidade de Agent Runner integrada ao AstrBot.

## Como usar

Por padrão, o AstrBot utiliza sua IA integrada. Selecione um modelo de chat em **Config → AI → Model** e configure personas, bases de conhecimento e ferramentas conforme necessário.

Para conectar um aplicativo externo, selecione o modo de execução e informe os dados de conexão diretamente no perfil de configuração atual:

1. Abra **Config** na barra lateral da WebUI, selecione o perfil que deseja editar e entre em **AI**.
2. Clique em **More actions** (`…`) ao lado do título de AI e, em seguida, em **Change Execution Mode**.
3. Escolha Dify, Coze, Alibaba Cloud Bailian ou DeerFlow. Leia e marque a confirmação de redefinição da configuração e clique em **Use This Mode**.
4. Confirme que **Enable AI** está ativado. Informe a chave de API, o ID da aplicação, o endpoint da API e os demais campos exibidos para o modo escolhido. Consulte os guias de integração abaixo para saber como preencher cada campo.
5. Clique em **Save Configuration**, no canto inferior direito, para aplicar as alterações.

> [!IMPORTANT]
> Ao trocar de modo, as configurações do modo de execução atual são substituídas pelos valores padrão do novo modo. Se você voltar ao modo anterior, precisará configurá-lo novamente. Para preservar as configurações originais, duplique o perfil em **Manage Configurations...** antes de trocar de modo.

A WebUI atual não exige a criação de um Agent Runner em **Providers** nem a seleção de um ID de provedor de executor. Cada perfil armazena seu próprio modo de execução e seus dados de conexão. Use perfis separados quando bots diferentes precisarem se conectar a aplicativos distintos.

## Guias de integração

Os guias específicos destes provedores ainda estão disponíveis em inglês:

- [Dify](/en/providers/agent-runners/dify.md)
- [Coze](/en/providers/agent-runners/coze.md)
- [Aplicativo Alibaba Cloud Bailian](/en/providers/agent-runners/dashscope.md)
- [DeerFlow](/en/providers/agent-runners/deerflow.md)
