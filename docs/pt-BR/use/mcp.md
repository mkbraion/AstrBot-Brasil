# MCP

MCP (Model Context Protocol, Protocolo de Contexto de Modelo) é um protocolo aberto que conecta aplicações de IA a ferramentas externas e serviços de dados. Pense em um servidor MCP como um conjunto de ferramentas que uma IA pode chamar: o servidor fornece os recursos, enquanto o AstrBot se conecta a ele, disponibiliza suas ferramentas ao Agent e usa os resultados para responder ao usuário.

Por exemplo, um servidor de pesquisa de artigos permite que o Agent responda a “Encontre artigos recentes sobre RAG” realizando uma pesquisa de verdade. Um servidor de calendário pode permitir a consulta de compromissos. As ações disponíveis dependem das ferramentas do servidor e das permissões da conta. O MCP não concede automaticamente acesso a todos os sites ou computadores.

## Antes de começar {#initial-configuration}

- Configure um modelo de chat funcional que ofereça suporte a chamadas de ferramentas e use o modo de execução da IA integrada do AstrBot. O suporte nos modos de execução de Agents de terceiros depende da integração de cada um.
- Escolha um servidor MCP e leia as instruções dele sobre transporte, configuração, dependências e requisitos de token de acesso.
- Confirme se ele fornece as **ferramentas** de que você precisa. Esta integração tem como objetivo principal disponibilizar ferramentas MCP ao Agent do AstrBot.

O MCP funciona em conjunto com [plugins](/en/use/plugin) e [Skills](/en/use/skills): plugins ampliam os comandos e o tratamento de mensagens do AstrBot; o MCP conecta ferramentas fornecidas por serviços independentes; Skills oferecem fluxos de trabalho reutilizáveis para tarefas.

## Escolher um método de conexão

Abra `Extensions → MCP Servers` na WebUI. A entrada que antes aparecia na página independente de ferramentas agora fica na aba MCP do espaço de trabalho Extensions.

O AstrBot oferece suporte a três tipos de transporte. **Se um provedor fornecer um endpoint remoto, comece por Streamable HTTP. Esse método não exige uma instalação local de Node.js ou uv.**

| Transporte | Quando usar | O que preparar |
| --- | --- | --- |
| Streamable HTTP | Serviço de um provedor ou servidor MCP implantado remotamente | Endpoint MCP e cabeçalhos de autenticação opcionais |
| SSE | Servidor remoto que utiliza o transporte SSE mais antigo | Endpoint SSE e cabeçalhos de autenticação opcionais |
| stdio | Iniciar um programa MCP no ambiente de execução do AstrBot | Python, uv, Node.js ou outras dependências exigidas pelo servidor |

Use o transporte especificado pelo servidor. A URL de uma página comum ou de uma API REST não é necessariamente um endpoint MCP; um endpoint SSE não é intercambiável com um endpoint Streamable HTTP.

### Preparar um ambiente stdio

**Instale somente o que o servidor escolhido exigir.** Servidores Python podem usar `uv` / `uvx`, enquanto servidores Node.js geralmente usam `npx`. Conexões remotas não exigem a instalação dos dois.

Instale as dependências **no ambiente em que o AstrBot é executado**. Em uma implantação a partir do código-fonte, use a mesma conta e o mesmo ambiente do AstrBot. No Docker, instale-as dentro do contêiner; instalá-las somente no host não é suficiente.

A imagem Docker oficial criada a partir do repositório atual inclui Node.js e uv. Imagens antigas ou de terceiros podem ser diferentes. Verifique primeiro, substituindo `astrbot` pelo nome do seu contêiner:

```bash
docker exec astrbot uv --version
docker exec astrbot node --version
docker exec astrbot npx --version
```

Se o uv estiver ausente, use `Install pip Package` em `Data & Logs → Logs` para instalar `uv` ou execute:

```bash
docker exec astrbot python -m pip install uv
```

Para usar Node.js em uma implantação a partir do código-fonte, siga as [instruções de download do Node.js](https://nodejs.org/en/download). No Docker, atualize para uma imagem que contenha as dependências necessárias ou adicione-as ao seu Dockerfile. Pacotes instalados manualmente dentro de um contêiner podem desaparecer quando ele for recriado.

Se o AstrBot não encontrar um comando recém-instalado, reinicie o AstrBot para que ele reconheça as alterações no ambiente ou use um caminho absoluto para o executável em `command`. Em JSON, escape os caminhos do Windows, por exemplo, `C:\\tools\\node.exe`.

## Adicionar seu primeiro servidor MCP {#installing-mcp-servers}

1. Abra `Extensions → MCP Servers` e clique no botão **+**, no canto inferior direito.
2. Informe um **Server Name** fácil de reconhecer, como `arxiv`.
3. Escolha o modelo apropriado, cole o JSON do servidor em **Server Configuration** e substitua os endpoints, caminhos e tokens de exemplo.
4. Clique em **Test Connection** para verificar a conectividade e descobrir as ferramentas disponíveis.
5. Clique em **Save**. Ao adicionar um servidor, o AstrBot verifica a conexão novamente e se conecta a ele. A lista deverá exibir **Connected** e as ferramentas disponíveis.

![Janela de configuração para adicionar um servidor MCP (captura da interface em inglês)](/en/use/images/mcp-config-en.png)

Adicione um servidor por vez. Se um serviço fornecer uma configuração completa envolvida em `mcpServers`, você poderá colar o objeto de configuração de um servidor. O AstrBot também aceita o formato com esse invólucro, mas uma única operação de adição não importa todos os servidores contidos nele.

### Exemplo de Streamable HTTP remoto

Este exemplo ilustra o formato de configuração. `example.com` é um placeholder e não pode ser usado em um teste de conexão real. Use o endpoint e o método de autenticação fornecidos pelo seu serviço:

```json
{
  "transport": "streamable_http",
  "url": "https://example.com/mcp",
  "headers": {
    "Authorization": "Bearer YOUR_TOKEN"
  },
  "timeout": 30,
  "sse_read_timeout": 300
}
```

Se a autenticação não for necessária, remova `headers` ou defina-o como `{}`. Para um servidor SSE, altere `transport` para `sse` e informe o endpoint SSE correspondente.

### Exemplo stdio: pesquisar artigos {#an-example}

O [arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) documenta uma configuração de inicialização baseada em uv:

```json
{
  "command": "uv",
  "args": [
    "tool",
    "run",
    "arxiv-mcp-server",
    "--storage-path",
    "data/arxiv"
  ]
}
```

A primeira inicialização pode baixar dependências. Consulte o README mais recente do servidor para obter os argumentos atuais. No Docker, armazene artigos baixados e outros arquivos persistentes no diretório `data` montado, usando caminhos do contêiner.

Para variáveis de ambiente, use diretamente o objeto JSON `env`. Este é apenas um exemplo de formato; substitua o comando, o pacote e os nomes das variáveis pelos exigidos pelo seu servidor:

```json
{
  "command": "uvx",
  "args": ["your-mcp-package"],
  "env": {
    "API_TOKEN": "YOUR_TOKEN",
    "API_URL": "https://example.com"
  }
}
```

`command` identifica um executável, e `args` contém argumentos separados, não um comando de shell completo. As versões atuais validam os inicializadores stdio. O exemplo antigo `command: "env"` e wrappers de shell, como `bash -c`, não são compatíveis; coloque as variáveis de ambiente em `env`.

> [!NOTE]
> stdio inicia um processo local no ambiente de execução do AstrBot. Use servidores confiáveis e configure as permissões conforme necessário. As configurações de isolamento local do Agent não isolam automaticamente esse processo do servidor MCP.

## Permitir que o Agent use ferramentas MCP

Depois de conectar o servidor, confirme se as ferramentas estão disponíveis para a conversa atual:

1. Abra **Personas** e edite a Persona usada pela conversa.
2. Em **Persona Capabilities**, localize o servidor MCP na lista de ferramentas. Selecione o servidor inteiro ou use o botão de engrenagem para escolher ferramentas individuais; depois, salve a Persona.
3. Confirme se a conversa está usando essa Persona e descreva a tarefa naturalmente, por exemplo: “Pesquise artigos recentes sobre RAG multimodal e me informe os títulos e links”.

A Persona padrão usa todos os recursos disponíveis. Crie ou edite uma Persona personalizada para restringir a seleção. Selecionar em uma Persona uma ferramenta desabilitada globalmente não a habilita novamente.

**Estar conectado significa que o serviço está acessível; isso não garante que o modelo chamará uma ferramenta.** O uso de ferramentas depende do modelo, da Persona, da tarefa e das descrições das ferramentas. Ferramentas externas, como pesquisas MCP, não exigem Computer Use. Configure um [ambiente de execução e suas permissões](/pt-BR/use/astrbot-agent-sandbox) somente quando o próprio AstrBot precisar executar código ou acessar arquivos.

## Gerenciar e sincronizar servidores

- **Ver ferramentas:** clique na quantidade de ferramentas disponíveis para consultar os nomes das ferramentas do servidor.
- **Editar:** clique na entrada de um servidor, atualize seu JSON e salve.
- **Conectar / Desconectar:** use a chave à direita. As ferramentas ficam indisponíveis enquanto o servidor estiver desconectado.
- **Excluir:** remova do AstrBot a configuração do servidor. Isso não desinstala um programa stdio nem exclui um serviço remoto.
- **Sincronizar do ModelScope:** use o botão de sincronização no canto inferior direito. Siga a janela para obter um token de acesso pessoal e sincronizar servidores. Primeiro, configure no ModelScope os serviços MCP desejados.

## Solução de problemas

| Sintoma | O que verificar primeiro |
| --- | --- |
| JSON inválido | Aspas ausentes, vírgulas finais ou texto explicativo colado na configuração |
| `uv`, `npx` ou `node` não encontrado | Se o executável está disponível no ambiente do AstrBot; usuários do Docker precisam verificar dentro do contêiner |
| Comando stdio não permitido | Não coloque um comando de shell completo em `command`; use o inicializador Python/Node.js/uv compatível e coloque as variáveis em `env` |
| Serviço remoto retorna 401 / 403 | Validade do token e cabeçalhos de autenticação exigidos pelo provedor |
| Docker não consegue acessar `localhost` | Dentro de um contêiner, `localhost` significa o próprio contêiner. Use um endereço de host acessível; o Docker Desktop normalmente oferece suporte a `host.docker.internal` |
| Conectado, mas sem ferramentas | Se o servidor fornece ferramentas MCP e se a conta tem permissão; consulte os logs do servidor e `Data & Logs → Logs` |
| Existem ferramentas, mas o Agent não as chama | Suporte do modelo a chamadas de ferramentas, seleção da Persona e estado global das ferramentas; teste uma tarefa que claramente exija a ferramenta |
| A ferramenta expira por tempo limite | Diferencie atrasos de conexão de uma execução lenta da ferramenta. As configurações de conexão ficam no JSON do MCP; procure em Config a configuração de tempo limite das chamadas de ferramentas para ajustar a execução |

Oculte tokens reais antes de compartilhar configurações, capturas de tela ou logs. Mantenha visíveis os nomes dos campos ao solicitar ajuda para solucionar problemas.

## Para saber mais

- [Documentação oficial do MCP](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Exemplos oficiais de servidores MCP](https://github.com/modelcontextprotocol/servers)
- [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)
- [Diretório MCP do ModelScope](https://www.modelscope.cn/mcp)
