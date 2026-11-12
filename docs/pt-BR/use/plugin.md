---
outline: deep
---

# Plugins do AstrBot {#astrbot-star}

Plugins são extensões que adicionam recursos ao AstrBot. Eles podem disponibilizar comandos de chat, conectar serviços externos ou fornecer novas ferramentas a agentes de IA, sem exigir alterações no próprio AstrBot.

Por exemplo, se você quer que seu bot consulte a previsão do tempo, assine atualizações, gere imagens ou interaja com um serviço pelo chat, procure um plugin adequado no mercado. **Em geral, usar plugins não exige programação. Criar ou modificar um plugin, sim.**

Este guia começa pela instalação e pelo uso cotidiano. Se quiser desenvolver um plugin, consulte o [Guia de desenvolvimento de plugins](/en/dev/star/plugin-new.html) (em inglês).

## O que são plugins e o que eles podem fazer?

O AstrBot cuida das funções básicas: receber mensagens, conectar modelos e gerenciar conversas. Os plugins usam as APIs do AstrBot para acrescentar funcionalidades a esses fluxos. Na documentação de desenvolvimento e no código, os plugins também são chamados de **Stars**.

| Recurso | Como funciona e exemplos |
| --- | --- |
| Comandos de chat | Um comando específico aciona um recurso, como consultar informações, gerar conteúdo ou executar uma tarefa administrativa. Cada plugin define os nomes e os argumentos de seus comandos. |
| Ferramentas de IA | Um agente pode chamar ferramentas para realizar tarefas, como obter dados de um serviço. O usuário descreve o que precisa em linguagem natural, e o modelo decide se deve chamar uma ferramenta. |
| Processamento de mensagens | Plugins escutam mensagens ou outros eventos, respondem a conteúdos que correspondam a determinadas condições ou modificam solicitações e respostas da IA. |
| Integrações externas | Plugins conectam APIs de terceiros, bancos de dados ou sistemas empresariais. Algumas integrações exigem uma chave de API, uma conta ou o endereço de um serviço. |
| Páginas de gerenciamento e Skills | Plugins podem fornecer páginas próprias na WebUI e incluir Skills que orientam agentes na execução de tarefas específicas. |

Esses são recursos do sistema de plugins; **um plugin individual não necessariamente oferece todos eles**. Consulte a documentação do autor para verificar funcionalidades, plataformas compatíveis, requisitos de modelo e configurações.

::: tip Todos os plugins precisam de IA?
Plugins de comandos e de processamento de mensagens não precisam necessariamente de um modelo de IA. Plugins que fornecem ferramentas de IA normalmente exigem um modelo compatível com chamadas de ferramentas e uma Persona que permita o uso das ferramentas correspondentes. Instalar um plugin não faz com que todos os seus recursos participem automaticamente de todas as conversas.
:::

## Primeiros passos: instale seu primeiro plugin

Para instalar seu primeiro plugin, use o mercado de plugins e siga o fluxo completo abaixo.

### 1. Abra o mercado de plugins

Na WebUI do AstrBot, selecione **Extensões** na barra lateral, abra a aba **Plugins** e mude para **AstrBot Plugin Market**.

- **Instalados**: gerencie os plugins instalados nesta instância do AstrBot.
- **AstrBot Plugin Market**: explore, pesquise e instale plugins.

Esse mesmo espaço de trabalho também tem as abas **Skills**, **Servidores MCP** e **Manipuladores**, destinadas a Skills, servidores MCP e comandos, ferramentas e outros manipuladores registrados.

### 2. Escolha um plugin adequado

Pesquise pelo nome do plugin ou por uma palavra-chave que descreva o recurso desejado. Você também pode filtrar por categorias, como aprimoramento de IA, entretenimento, produtividade, integrações, utilitários e outras. Abra os detalhes do plugin e confira:

- **Recursos e modo de uso**: verifique se ele atende à sua necessidade e se é utilizado por comandos, linguagem natural ou outro tipo de acionamento.
- **Plataformas compatíveis**: confirme se funciona com sua plataforma de mensagens. Alguns recursos dependem de APIs específicas da plataforma.
- **Requisitos de versão do AstrBot**: confira se a versão instalada é compatível.
- **Configuração e dependências**: verifique se são necessárias uma chave de API, um serviço externo, um programa adicional ou condições específicas de implantação.

Se a descrição estiver incompleta, abra o repositório e leia o README e a documentação de uso. Estrelas, downloads e datas de atualização ajudam na pesquisa, mas não substituem a verificação de compatibilidade nem as instruções de uso.

### 3. Instale e verifique se o plugin é carregado

Clique em **Instalar**, confirme a origem da instalação e aguarde a conclusão da operação. Volte à página **Instalados**, localize o plugin e confira se ele está aberto e não apresenta erros de carregamento.

Se ele aparecer em **Falha ao carregar plugins**, leia o erro, siga as [orientações de solução de problemas](#solucao-de-problemas) e clique em **Recarregar** depois de corrigir o problema.

### 4. Configure o plugin

Se houver configurações obrigatórias, clique no ícone de engrenagem (**Configurar**) no cartão do plugin, preencha os parâmetros descritos pelo autor e salve. Integrações externas podem exigir uma chave de API, o endereço de um serviço ou um destino de assinatura.

Se o plugin não tiver configurações adicionais, ignore esta etapa. As credenciais solicitadas por um plugin devem ser informadas na configuração dele, e não em configurações de modelo que não tenham relação com o serviço.

### 5. Experimente o recurso mais simples

Em uma plataforma de mensagens conectada ao AstrBot, siga as instruções do plugin para testar uma funcionalidade básica:

- **Plugins de comandos**: envie o comando documentado e seus argumentos. Envie <code>/help</code> para consultar os comandos habilitados no momento ou gerencie-os em **Extensões → Manipuladores → Comando**.
- **Plugins com ferramentas de IA**: descreva sua solicitação ao bot. Confira se o modelo atual oferece suporte a chamadas de ferramentas e se a Persona atual permite o uso da ferramenta.
- **Plugins baseados em eventos**: provoque o evento documentado, por exemplo, enviando uma mensagem que corresponda a uma regra.

::: info Prefixos de comando
Os exemplos deste guia usam o prefixo padrão <code>/</code>. Se você alterou o prefixo de ativação para <code>!</code>, use <code>!help</code> e o mesmo prefixo nos comandos do plugin. Alguns comandos exigem permissões de administrador do AstrBot; consulte a documentação do plugin e as configurações de gerenciamento de comandos.
:::

## O mercado de plugins

O mercado permite descobrir e instalar plugins da comunidade. Os plugins instalados são gerenciados na página **Instalados** e são executados no ambiente do seu AstrBot, não dentro do mercado.

O mercado oferece pesquisa, categorias e opções de ordenação. Em geral, iniciantes podem usar a **fonte padrão de plugins**. Se necessário, acesse o gerenciamento de fontes para adicionar ou alternar fontes personalizadas. Uma fonte determina a lista de plugins que você pode explorar; adicionar uma fonte não instala todos os plugins dela.

::: warning Entenda a origem antes de instalar
Os plugins são executados no ambiente Python do AstrBot. Instale plugins somente de fontes nas quais você confia. A presença de um plugin no mercado não garante estabilidade nem segurança. As configurações de isolamento local do Agent restringem a execução do agente; elas não isolam automaticamente o código arbitrário de plugins.
:::

Para autores, a opção **Enviar minha extensão**, no final do mercado, abre a [página de publicação do AstrBot Cloud](https://cloud.astrbot.app/publish). Consulte o [guia de publicação de plugins](/en/dev/star/plugin-publish.html) (em inglês) para conhecer o processo completo.

## Instalar a partir de um repositório ou arquivo

Você pode instalar manualmente um plugin que não esteja listado no mercado ou um pacote específico fornecido pelo autor. Clique no botão **Instalar (+)**, no canto inferior direito da página de plugins instalados ou do mercado.

### Instalar a partir de uma URL

1. Selecione **Instalar a partir de URL**.
2. Informe a URL do repositório Git do plugin fornecida pelo autor, por exemplo, <code>https://github.com/autor/repositorio-do-plugin</code>.
3. Confirme a origem, instale e confira o estado do plugin na página **Instalados**.

Use a URL do repositório de código, não o endereço de um tutorial, da WebUI ou de uma página qualquer.

### Instalar a partir de um arquivo

1. Obtenha o pacote <code>.zip</code> do plugin fornecido pelo autor.
2. Selecione **Instalar a partir de arquivo**, envie o ZIP e instale-o.
3. Confira se o plugin foi carregado; em seguida, configure-o e utilize-o conforme a documentação.

O arquivo compactado precisa conter um plugin completo do AstrBot. Um arquivo Python isolado, uma configuração MCP ou um pacote de Skills não é um pacote de instalação de plugin. A instalação a partir de um arquivo também não garante funcionamento offline: instalar dependências ou acessar serviços externos ainda pode exigir conexão com a rede.

## Configuração e gerenciamento

### Configurações e disponibilidade dos plugins

As configurações a seguir controlam aspectos diferentes:

| Local | O que controla |
| --- | --- |
| Extensões → Plugins → ícone de engrenagem do plugin | Os parâmetros do próprio plugin, como endereços de serviços, credenciais e opções de recursos. Em geral, eles são compartilhados por toda a instância do AstrBot; o plugin pode implementar configurações mais específicas. |
| Configuração → selecione um perfil → Plugin | Quais plugins podem ser usados por aquele perfil. Por padrão, são usados todos os plugins que não foram fechados; você pode selecionar apenas alguns. Salve o perfil depois de fazer alterações. |
| Configurações de recursos da Persona | Quais ferramentas e Skills a Persona atual pode utilizar. Para plugins com ferramentas de IA, confira se a ferramenta correspondente está permitida aqui. |
| Extensões → Manipuladores | Comandos registrados, ferramentas de função e outros manipuladores. Os comandos podem ter estado de habilitação, nome e permissões próprios. |

**Primeiro confira se o plugin está aberto; depois, verifique o perfil e a Persona usados pela conversa atual.** Selecionar em um perfil um plugin que está fechado não o abre. Se você direciona plataformas ou conversas para perfis diferentes, edite o perfil que realmente se aplica àquela conversa.

### Atualizar, recarregar, fechar ou excluir

Na página **Instalados**, você pode executar as seguintes ações:

| Ação | Quando usar |
| --- | --- |
| Atualizar | Baixa o novo código disponibilizado pelo autor. Leia as alterações antes de atualizar e faça backup das configurações e dos dados de plugins importantes. |
| Recarregar | Carrega novamente o código existente, por exemplo, depois de corrigir dependências ou editar código. Recarregar não baixa uma versão nova. |
| Abrir / Fechar plugin | Ativa ou interrompe o plugin. Feche-o temporariamente quando não precisar dele, mantendo os arquivos para uso posterior. |
| Manipuladores | Consulta os comandos, as ferramentas e outros manipuladores registrados pelo plugin. |
| Excluir | Desinstala um plugin. A caixa de diálogo permite escolher separadamente se as configurações e os dados persistentes também devem ser excluídos. |

Preste atenção às opções de exclusão dos arquivos de configuração e dos dados persistentes do plugin. Se quiser manter as configurações ou os dados de negócio, deixe desmarcada a opção correspondente.

## Plugins, MCP e Skills

| Extensão | Finalidade principal | Saiba mais |
| --- | --- | --- |
| Plugins | Extensões Python integradas aos fluxos de mensagens e de IA do AstrBot, com comandos, ferramentas, manipuladores de eventos, páginas e outros recursos. | Esta página e o [guia de desenvolvimento de plugins](/en/dev/star/plugin-new.html) (em inglês) |
| MCP | Conecta serviços de ferramentas independentes pelo protocolo MCP para que os modelos possam chamar essas ferramentas. | [MCP](/pt-BR/use/mcp) |
| Skills | Fornece instruções de tarefas, fluxos de trabalho, materiais de referência e scripts para orientar um agente. | [Skills](/en/use/skills.html) (em inglês) |

Esses recursos podem trabalhar em conjunto. Um plugin pode fornecer ferramentas e incluir uma Skill que explique como utilizá-las. As Skills incluídas em plugins aparecem em **Extensões → Skills** e podem ser habilitadas ou desabilitadas. Seus arquivos são gerenciados pelo plugin e não podem ser editados ou excluídos diretamente pela página local de Skills.

## Solução de problemas {#solucao-de-problemas}

### A instalação falha ou o mercado não carrega

Leia o erro e os logs exibidos na janela de instalação. Em caso de tempo limite de download ou falha de conexão, verifique se **o dispositivo ou contêiner no qual o AstrBot está sendo executado** consegue acessar a fonte do plugin, o repositório de código e os serviços de download de dependências. Conseguir acessar esses endereços pelo navegador não comprova que o ambiente do AstrBot também consiga.

Em instalações por URL, confira o endereço do repositório. Em instalações por arquivo, verifique se o ZIP está completo. Se aparecer um aviso de incompatibilidade de versão, confira os requisitos e escolha versões compatíveis do AstrBot e do plugin.

### Um plugin não consegue ser carregado

Leia o erro em **Falha ao carregar plugins** ou abra **Dados e logs → Logs** para consultar os detalhes.

- **Dependência Python ausente**: instale a dependência conforme a documentação do plugin. A página de logs também oferece uma opção para instalar pacotes Pip. Instale no ambiente Python que realmente executa o AstrBot; com Docker, instalar o pacote somente no sistema hospedeiro não é suficiente.
- **Programa ou serviço externo ausente**: configure o programa, a conta ou o serviço exigido conforme a documentação do plugin.
- **Erros de código ou versões incompatíveis**: confira as versões do plugin e do AstrBot, consulte problemas conhecidos e entre em contato com o autor se necessário.

Depois de corrigir o problema, clique em **Recarregar**. Não é necessário reiniciar todo o processo do AstrBot apenas para recarregar um plugin que falhou.

### A instalação é concluída, mas o bot não responde

Verifique os itens nesta ordem:

1. O plugin está aberto e não apresenta erros de carregamento.
2. O perfil aplicado à conversa atual permite o uso do plugin.
3. Os parâmetros estão completos e os serviços externos necessários estão disponíveis.
4. O nome do comando, o prefixo, os argumentos, a plataforma e as permissões correspondem às instruções.
5. Para ferramentas de IA, o modelo atual oferece suporte a chamadas de ferramentas e a Persona atual permite o uso das ferramentas correspondentes.

Nem todo plugin oferece comandos de chat, e o modelo não chama todas as ferramentas disponíveis em todas as mensagens. Comece pelo exemplo mais simples fornecido pelo autor antes de testar solicitações mais complexas.

### Como relatar um problema?

Use a página de Issues do repositório do plugin ou o canal de suporte indicado pelo autor. Inclua a versão do AstrBot, a versão do plugin, a plataforma de mensagens, o método de implantação, as etapas para reproduzir o problema e os logs de erro relevantes. Não publique chaves de API, tokens nem outras credenciais.

## Desenvolva seu próprio plugin

Se os plugins existentes não atenderem às suas necessidades, você poderá criar um em Python. Recomenda-se ter conhecimentos básicos de Python e Git / GitHub. Siga este roteiro de aprendizado:

1. **Crie um projeto**: siga o [guia de desenvolvimento de plugins](/en/dev/star/plugin-new.html) (em inglês) e crie um repositório a partir do [modelo helloworld](https://github.com/Soulter/helloworld). Recomenda-se usar o prefixo <code>astrbot_plugin_</code> no nome.
2. **Prepare o ambiente de desenvolvimento**: coloque o repositório em <code>data/plugins/&lt;plugin-directory&gt;/</code> do AstrBot e preencha <code>metadata.yaml</code> para que o AstrBot identifique o nome, a versão, o autor e os demais metadados do plugin.
3. **Implemente um recurso mínimo**: comece com um comando que receba uma mensagem e envie uma resposta. Consulte [Como escutar eventos de mensagem](/en/dev/star/guides/listen-message-event.html) e [Como enviar mensagens](/en/dev/star/guides/send-message.html) (em inglês); depois, faça o teste com seu bot.
4. **Adicione recursos gradualmente**: introduza [ferramentas de IA e interação com modelos](/en/dev/star/guides/ai.html), [configuração de plugins](/en/dev/star/guides/plugin-config.html), [armazenamento de dados](/en/dev/star/guides/storage.html) ou [páginas de plugins](/en/dev/star/guides/plugin-pages.html) (em inglês) conforme necessário. Depois de alterar o código, recarregue o plugin pela WebUI.
5. **Documente o uso**: descreva no README os recursos, a instalação, os comandos ou as ferramentas, as configurações, as dependências, as plataformas compatíveis e os requisitos de versão. Declare as dependências Python necessárias e complete os metadados do plugin.
6. **Publique**: envie o código ao GitHub e siga o [guia de publicação](/en/dev/star/plugin-publish.html) (em inglês) para enviar o plugin pelo [AstrBot Cloud](https://cloud.astrbot.app/publish). A publicação exige uma conta no AstrBot Cloud.

O guia de desenvolvimento apresenta em detalhes a preparação do ambiente e o uso das APIs. Para criar seu primeiro plugin, faça um comando simples funcionar antes de adicionar configurações, ferramentas ou serviços externos; assim, fica mais fácil identificar e corrigir problemas.
