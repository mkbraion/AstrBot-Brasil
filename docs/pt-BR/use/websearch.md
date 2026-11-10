# Pesquisa na Web

A Pesquisa na Web permite que a IA integrada do AstrBot use um serviço de busca enquanto responde a perguntas. Ela pode encontrar notícias, atualizações de produtos e materiais públicos de referência — por exemplo, verificar o lançamento de um software, comparar opções ou ler uma página da Web e resumir seu conteúdo.

O modelo recupera os resultados e os utiliza para elaborar a resposta. A pesquisa complementa o conhecimento que o modelo já possui, mas os resultados ainda podem estar desatualizados ou incorretos. Abra as fontes para verificar informações importantes.

## O que você precisa

- **IA integrada do AstrBot**: habilite a IA em `Config → AI` e selecione AstrBot Built-in AI como modo de execução. A pesquisa em modos de terceiros, como Dify ou Coze, é configurada no serviço correspondente.
- **Um modelo de chat com chamada de ferramentas**: tanto o modelo quanto a API usada para acessá-lo precisam oferecer suporte a Function Calling / Tool Calling.
- **Um serviço de pesquisa**: escolha um provedor e obtenha uma chave de API, se necessário. As chaves de pesquisa e as chaves do modelo de chat são credenciais distintas.
- **Acesso à rede**: o servidor ou contêiner que executa o AstrBot precisa conseguir acessar a API do serviço selecionado.

A pesquisa utiliza ferramentas integradas. Você não precisa instalar um plugin de pesquisa nem usar o Computer Use. A permissão de rede para execução de código se aplica à execução de código, não às solicitações enviadas aos serviços de pesquisa.

## Habilitar a Pesquisa na Web

1. Abra `Config` na barra lateral e selecione o perfil realmente utilizado pela sua conversa.
2. Abra `AI → Capabilities` e localize `Web Search`.
3. Ative `Enable Web Search` e escolha um `Web Search Provider`.
4. Informe a chave de API do provedor. O Baidu AI Search utiliza uma única chave; os demais provedores aceitam uma lista. Uma chave é suficiente para começar, e várias chaves podem ser alternadas.
5. Clique em `Save Configuration` no canto inferior direito.

![Configurações de Pesquisa na Web (captura da interface em inglês)](/en/use/images/websearch-settings-en.png)

Essas configurações pertencem ao perfil selecionado. Alterar `default` não habilita a pesquisa para bots que utilizam outro perfil. Consulte o [guia da WebUI](/pt-BR/use/webui) para saber como atribuir perfis.

## Escolher um provedor de pesquisa

O AstrBot oferece suporte a sete provedores. Configure um deles para começar; você não precisa criar uma conta em todos os serviços.

| Provedor | Onde obter uma chave | Recursos disponíveis no AstrBot |
| --- | --- | --- |
| <span id="tavily">Tavily</span> | [Painel do Tavily](https://app.tavily.com/home) | Pesquisa na Web e extração do conteúdo de uma página a partir de uma URL |
| <span id="bocha">BoCha</span> | [BoCha](https://bochaai.com/) | Pesquisa na Web |
| <span id="baidu-ai-search">Baidu AI Search</span> | [Gerenciamento de chaves de API do Baidu Cloud](https://console.bce.baidu.com/iam/#/iam/apikey/list) | Pesquisa com Baidu AI Search; exige acesso ao serviço correspondente |
| <span id="brave">Brave</span> | [API do Brave Search](https://brave.com/search/api/) | Pesquisa na Web |
| <span id="firecrawl">Firecrawl</span> | [Firecrawl](https://firecrawl.dev/) | Pesquisa na Web e extração do conteúdo de uma página a partir de uma URL |
| <span id="exa">Exa</span> | [Painel do Exa](https://dashboard.exa.ai/) | Pesquisa por palavras-chave ou semântica, conteúdo de páginas e filtros como domínio e data |
| <span id="anysearch">AnySearch</span> | [Console do AnySearch](https://anysearch.com/console/api-keys) | Pesquisa geral e recuperação especializada para pesquisa acadêmica, documentação de código, finanças, informações jurídicas e outros domínios |

O AnySearch utiliza o modo anônimo com uma cota diária gratuita quando a lista de chaves está vazia. Os demais provedores exigem suas próprias chaves. Consulte o site de cada serviço para verificar as cotas, os preços, a disponibilidade regional e os requisitos de autorização atuais.

### Pesquisar um assunto ou ler um link

Pesquisar um assunto retorna resultados de um serviço de pesquisa. Resumir um link específico exige extrair o conteúdo daquela página. Atualmente, Tavily, Firecrawl e Exa oferecem ferramentas específicas para extração de páginas; escolha um deles se a leitura de links for uma tarefa frequente.

A extração não consegue ler todos os sites. Páginas protegidas por login ou paywall, sites com restrições contra bots e algumas páginas renderizadas por scripts podem não funcionar.

## Usar a pesquisa em uma conversa

Depois de salvar as configurações, envie ao bot ou ao ChatUI uma solicitação que deixe clara a intenção de pesquisar:

```text
Pesquise o lançamento mais recente do AstrBot. Informe a versão, resuma as principais alterações e inclua links para as fontes.
```

```text
Encontre a documentação oficial do bubblewrap e explique quais problemas essa ferramenta ajuda a resolver.
```

Com um provedor que ofereça extração de páginas, você também pode pedir:

```text
Leia esta página e resuma as etapas de instalação: https://docs.astrbot.app/pt-BR/deploy/astrbot/docker.html
```

O modelo decide se deve pesquisar, quais palavras-chave utilizar e se deve ler uma página em seguida. Habilitar a pesquisa não faz com que todas as mensagens acessem a Internet. Quando precisar de informações atuais, peça: “pesquise primeiro e depois responda”.

O ChatUI pode exibir referências às fontes retornadas por algumas ferramentas de pesquisa. O resultado depende do provedor, de o modelo citar corretamente os resultados e da plataforma de mensagens. Em plataformas como Telegram ou QQ, peça ao modelo que inclua os links das fontes diretamente na resposta.

## Solução de problemas

### O modelo responde sem pesquisar

Faça um teste com “realize uma pesquisa na Web antes de responder” e confira se:

1. A conversa utiliza o perfil que você editou e está com AstrBot Built-in AI selecionado.
2. O modelo de chat e sua API oferecem suporte a chamadas de ferramentas.
3. A chave foi salva e ainda há cota disponível no serviço de pesquisa.

### Erros de chave inválida, cota ou solicitação

Confira o erro em `Data & Logs → Logs`. Os códigos `401` e `403` geralmente indicam problemas com a chave ou com as permissões do serviço; `429` normalmente indica uma cota esgotada ou um limite de requisições. Em caso de timeout, verifique a conectividade do ambiente do AstrBot com a API de pesquisa. Não informe a chave do modelo de chat no campo destinado à chave de pesquisa.

### A pesquisa funciona, mas o resumo de um link falha

Confirme se o provedor oferece extração de conteúdo de páginas e tente acessar uma página pública que não exija login. Se apenas um site falhar, verifique as restrições de acesso desse site.

### O antigo provedor `default` parou de funcionar após uma atualização

O provedor de pesquisa legado `default` não é mais compatível. Selecione um provedor atual, informe suas credenciais, habilite a pesquisa novamente e salve a configuração.

## Recursos relacionados

- [Base de conhecimento](/pt-BR/use/knowledge-base): utilize manuais, perguntas frequentes e materiais internos enviados por você. A pesquisa na Web é útil para informações públicas que mudam com frequência.
- [Orquestração de SubAgents](/pt-BR/use/subagent): disponibilize recursos de pesquisa para um Agent responsável por coletar informações.
- [MCP](/pt-BR/use/mcp): adicione ferramentas de outros serviços de recuperação por meio de seus servidores MCP.
