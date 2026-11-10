# Base de conhecimento do AstrBot

Uma base de conhecimento permite que o AstrBot responda a perguntas usando materiais fornecidos por você. Envie manuais de produtos, perguntas frequentes, anotações de cursos ou documentação de projetos para que o Agent recupere trechos relevantes antes de elaborar uma resposta.

Por exemplo, envie um guia de integração da comunidade para que o bot possa responder a perguntas como “Como faço para participar do projeto?” ou “Onde posso relatar um problema?”, sem precisar incluir o documento inteiro no prompt da Persona.

Esse processo é chamado de geração aumentada por recuperação (RAG). Durante o envio, o AstrBot extrai o texto, divide o conteúdo em trechos e cria um índice. Durante a conversa, recupera os trechos relevantes e os encaminha ao modelo de chat. O envio de documentos não treina nem ajusta esse modelo; as respostas ainda podem conter erros.

## Entenda as três funções de modelo

| Modelo | Obrigatório? | Função |
| --- | --- | --- |
| Modelo de chat | Necessário para responder perguntas | Lê os trechos recuperados e gera a resposta |
| Modelo de embedding | Necessário para criar uma base de conhecimento | Converte documentos e consultas em vetores para recuperação semântica |
| Modelo de reranking | Opcional | Reavalia os trechos candidatos para colocar primeiro os mais relevantes |

Os modelos de embedding e de chat são configurados separadamente. Um modelo que oferece suporte apenas a chat não pode ser usado como modelo de embedding. Comece com um modelo de chat e um modelo de embedding; adicione o reranking mais tarde, se necessário.

Esta página aborda a base de conhecimento integrada atual do AstrBot, disponível desde a versão 4.5.0. Ela não exige um plugin de base de conhecimento.

## Etapa 1: configurar um modelo de embedding {#configuring-embedding-model}

1. Abra `Providers` na barra lateral.
2. Selecione a aba `Embedding`, clique em `Add` e escolha um provedor.
3. Informe o endpoint da API do serviço, a chave de API, o nome do modelo, as dimensões dos vetores e as demais configurações obrigatórias.
4. Salve e confirme se o provedor está disponível.

As integrações atuais incluem serviços compatíveis com OpenAI, Google Gemini, Ollama, Alibaba Cloud Model Studio e serviços de embedding da NVIDIA. Para `OpenAI Embedding`, use a URL base da API do serviço e o nome de um modelo de embedding, não o nome de um modelo de chat.

Em serviços locais, como o Ollama, o endpoint precisa estar acessível a partir do ambiente que executa o AstrBot. No Docker, `localhost` aponta para o contêiner do AstrBot, não automaticamente para a máquina host.

As dimensões dos vetores precisam corresponder à saída real do modelo. Vetores produzidos por modelos diferentes não são intercambiáveis; consulte a documentação do modelo do provedor se tiver dúvidas.

### Configurar um modelo de reranking (opcional) {#configuring-reranker-model-optional}

Para adicionar o reranking, crie e salve o provedor correspondente em `Providers → Rerank`. É possível criar uma base de conhecimento, enviar documentos e utilizá-la sem um modelo de reranking.

::: tip Para onde o conteúdo é enviado?
Quando você usa um serviço remoto de embedding, o texto dos documentos e as consultas de recuperação são enviados a esse serviço. Os trechos recuperados são enviados ao modelo de chat durante a elaboração da resposta. Escolha serviços de modelos adequados ao conteúdo que pretende processar.
:::

## Etapa 2: criar uma base de conhecimento {#creating-a-knowledge-base}

1. Abra `Knowledge Base` na barra lateral e clique em `Create Knowledge Base`.
2. Informe um nome fácil de reconhecer, como “Integração da comunidade”, e uma descrição.
3. Em `Embedding Model`, selecione o provedor que você configurou.
4. Se quiser, selecione um `Rerank Model`; caso contrário, deixe o campo vazio.
5. Clique em `Create`.

![Criação de uma base de conhecimento e seleção dos modelos (captura da interface em inglês)](/en/use/images/knowledge-base-create-en.png)

Você pode criar várias bases de conhecimento — por exemplo, uma para manuais de produtos e outra para regras da comunidade — e selecionar uma ou mais para cada conversa.

::: warning Alterar o modelo de embedding exige uma nova base de conhecimento
A seleção do modelo de embedding fica bloqueada depois da criação. Não altere o modelo nem as dimensões dos vetores do provedor usado por uma base existente: o índice se tornaria incompatível. Para trocar de modelo, adicione um novo provedor, crie uma nova base de conhecimento e envie novamente os documentos originais.
:::

## Etapa 3: enviar materiais {#uploading-files}

### Enviar arquivos

1. Abra a base de conhecimento e selecione `Documents`.
2. Clique em `Upload Document` e mantenha selecionada a aba `File Upload`.
3. Selecione os arquivos ou arraste-os para a janela. Você pode selecionar vários arquivos de uma vez.
4. Na primeira tentativa, mantenha as configurações padrão de divisão em trechos e de processamento em lotes; depois, clique em `Upload`.
5. Aguarde o fim da análise, da divisão em trechos e da geração dos embeddings. Confirme se a lista de documentos mostra os arquivos e a quantidade de trechos de cada um.

![Janela de envio de arquivos da base de conhecimento (captura da interface em inglês)](/en/use/images/knowledge-base-upload-en.png)

Os formatos aceitos são `.txt`, `.md`, `.markdown`, `.rst`, `.adoc`, `.pdf`, `.docx`, `.epub`, `.xls` e `.xlsx`. A interface de envio informa o limite máximo de 128 MB por arquivo. Divida coleções grandes por assunto para facilitar o processamento e a manutenção.

Os PDFs devem conter texto extraível. PDFs digitalizados ou compostos apenas por imagens não passam automaticamente por OCR; converta-os primeiro em texto ou em PDFs pesquisáveis. Layouts complexos de documentos e planilhas também podem afetar a extração. Inspecione os trechos depois do envio.

### Escolher as configurações de divisão em trechos

A divisão em trechos separa documentos longos em passagens adequadas para recuperação.

| Configuração | Finalidade | Recomendação inicial |
| --- | --- | --- |
| Chunk Size | Controla o tamanho da passagem em caracteres | Comece com o padrão 512 e ajuste conforme os resultados |
| Chunk Overlap | Preserva o contexto compartilhado entre trechos adjacentes | Comece com 50; mantenha um valor menor que o tamanho do trecho |
| Batch Size | Quantidade de trechos enviados ao serviço de embedding por lote | Mantenha o padrão 32 |
| Concurrent Tasks Limit | Limita a quantidade de tarefas processadas simultaneamente | Comece com 3; reduza se o serviço limitar as solicitações |
| Max Retries | Quantidade de novas tentativas para tarefas com falha | Mantenha o padrão 3 |

Alterar as configurações padrão de divisão de uma base afeta os próximos envios. Isso não divide novamente os documentos já existentes. Envie os documentos outra vez se precisar alterar a divisão em trechos.

### Importar a partir de uma URL da Web

Altere a janela de envio para `From URL` e informe a URL de uma página pública. Esse recurso ainda está em versão beta e usa o **Tavily** para extrair o conteúdo HTML. Ele lê a chave do Tavily do **perfil padrão**. Siga a orientação da interface para configurar essa chave; credenciais de outro provedor de pesquisa não podem substituí-la.

A opção `Enable Content Cleaning` usa opcionalmente o modelo de chat selecionado para limpar e organizar o conteúdo extraído, gerando chamadas adicionais ao modelo. Páginas que exigem login, bloqueiam rastreadores ou não permitem a extração podem não ser importadas. O conteúdo importado é uma cópia do estado da página naquele momento; alterações posteriores no site não são sincronizadas automaticamente.

## Etapa 4: testar primeiro a recuperação

Um envio bem-sucedido não habilita automaticamente a base de conhecimento no chat. Primeiro, abra a aba `Retrieval` da base:

1. Digite uma pergunta cuja resposta esteja em um documento, como “Como uma pessoa nova pode participar do projeto?”.
2. Clique em `Search` e inspecione os trechos e os documentos de origem.
3. Confirme se os trechos contêm a resposta antes de conectar a base ao chat.

Esta página testa a recuperação, não a resposta gerada pelo modelo de chat. Se nenhum trecho relevante aparecer, verifique primeiro os documentos e os trechos.

## Etapa 5: usar em uma conversa {#using-the-knowledge-base}

1. Abra `Config` e escolha o perfil realmente utilizado pelo seu bot ou pela ChatUI.
2. Em `AI → Capabilities → Knowledge Base`, selecione uma ou mais entradas em `Knowledge Base List`.
3. Na primeira tentativa, mantenha as quantidades padrão de resultados recuperados.
4. Clique em `Save Configuration`, na parte inferior direita.
5. Na conversa correspondente, faça uma pergunta sobre o material enviado.

```text
Usando o guia de integração da comunidade, explique como participar do projeto. Se o material não abordar algum detalhe, informe isso.
```

Os documentos não se tornam memória permanente do modelo. A base de conhecimento relevante precisa ser selecionada pelo perfil atual ou por uma regra de sessão. Perfis diferentes podem usar bases diferentes; criar uma base não a habilita para todos os bots.

### Recuperação padrão e recuperação agêntica

| Modo | Quando ocorre a recuperação | Requisito do modelo de chat |
| --- | --- | --- |
| Recuperação padrão (default) | Recupera conteúdo usando a mensagem atual e acrescenta os trechos relevantes à solicitação enviada ao modelo | Não exige chamadas de ferramentas da base de conhecimento |
| `Agentic Knowledge Base Retrieval` | Disponibiliza a recuperação como ferramenta; o modelo decide quando e como consultá-la | O modelo e sua API precisam oferecer suporte a chamadas de ferramentas |

Mantenha o modo padrão se quiser recuperar conteúdo antes de cada resposta. Com a recuperação agêntica habilitada, o modelo pode responder sem consultar a base de conhecimento. Para testar, peça explicitamente que ele faça a consulta primeiro.

### Ajustar a quantidade de resultados

`Fusion Search Results Count` controla a quantidade de candidatos depois que os resultados de várias bases de conhecimento são combinados. `Final Results Count` controla quantos trechos são enviados ao modelo. Os valores padrão são 20 e 5.

Poucos resultados podem deixar uma resposta de fora; muitos resultados aumentam o tamanho da entrada e o ruído. Comece pelos valores padrão e ajuste conforme os trechos efetivamente retornados pelo teste de recuperação.

### Escolher uma base de conhecimento para um grupo ou conversa privada

Em `Custom Rules`, atribua bases de conhecimento e uma quantidade de resultados de recuperação a uma origem específica de mensagens. As seleções da sessão substituem as do perfil. Limpar a seleção e salvar remove a substituição e restaura as bases do perfil. Consulte [Regras personalizadas](/en/use/custom-rules).

## Manter uma base de conhecimento

- **Inspecionar documentos**: use a ação de visualização de um documento em `Documents` para conferir os trechos extraídos.
- **Atualizar materiais**: exclua o documento desatualizado e envie sua versão substituta para evitar que versões contraditórias sejam recuperadas juntas. Guarde cópias dos originais.
- **Ajustar a recuperação**: em `Settings`, ajuste a quantidade de resultados de recuperação densa e esparsa ou selecione um provedor de reranking. A recuperação densa prioriza a similaridade semântica; a esparsa prioriza a correspondência de palavras.
- **Renomear com cuidado**: os perfis selecionam bases de conhecimento pelo nome; portanto, atualize os perfis afetados depois de renomear uma base.
- **Excluir com cuidado**: excluir um documento remove seus trechos. Excluir uma base de conhecimento remove seus documentos e seu índice. Essas operações não podem ser desfeitas; faça backups antes.

## Solução de problemas

### A criação ou o envio falha

Verifique se o provedor de embedding está salvo e disponível, se o nome do modelo, o endpoint e as dimensões estão corretos e se a chave tem cota disponível. Consulte o erro em `Data & Logs → Logs`. Reduza o tamanho do lote ou a quantidade de tarefas simultâneas se o serviço limitar as solicitações.

### O envio foi concluído, mas a recuperação não encontra a resposta

Inspecione os trechos. O texto foi extraído corretamente? Ele contém as palavras-chave relevantes? O PDF é composto apenas por imagens digitalizadas? Tente uma pergunta mais específica em `Retrieval`; depois, ajuste a divisão em trechos, a quantidade de resultados ou adicione um modelo de reranking, se necessário.

### O teste de recuperação funciona, mas o bot não usa a resposta

Verifique a seleção de perfil da conversa e eventuais substituições de sessão. No modo agêntico, confirme também se o modelo e sua API oferecem suporte a chamadas de ferramentas. Mesmo assim, o modelo pode ignorar o material recuperado; uma instrução na Persona, como “Dê preferência às fontes recuperadas e não invente detalhes quando elas forem insuficientes”, pode ajudar.

### Erros de dimensão vetorial depois de trocar de modelo

O índice existente é incompatível com o novo modelo de embedding. Restaure as configurações originais do provedor ou crie uma nova base de conhecimento e envie novamente os documentos usando o novo modelo. Alterar apenas o campo de dimensão não converte os vetores armazenados.

## Exemplo: embeddings do SiliconFlow

Com o [SiliconFlow](https://cloud.siliconflow.cn/), obtenha uma chave no console do serviço e adicione um provedor `OpenAI Embedding`:

- Chave de API: sua chave do SiliconFlow.
- URL base da API: `https://api.siliconflow.cn/v1`.
- Modelo: um modelo de embedding oferecido atualmente pelo serviço, como `BAAI/bge-m3`; defina as dimensões conforme a documentação desse modelo.

Os modelos disponíveis, os preços e as cotas gratuitas podem mudar. Consulte as informações atuais da plataforma e, em seguida, siga as etapas de criação, envio e teste de recuperação descritas acima.

Você também pode habilitar a [Pesquisa na Web](/pt-BR/use/websearch) para obter informações públicas atualizadas. A base de conhecimento é indicada para materiais que você mantém; os dois recursos são complementares.
