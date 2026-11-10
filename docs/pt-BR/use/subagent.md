# Orquestração de SubAgents {#agent-handoff-and-subagent}

Um SubAgent é um assistente de IA com uma responsabilidade específica. O Agent principal conversa com o usuário, delega tarefas adequadas a um SubAgent e continua a resposta usando o resultado recebido.

<span id="motivation"></span>

Por exemplo, um SubAgent pode pesquisar fontes enquanto outro organiza arquivos. Cada um usa seu próprio prompt de Persona e sua própria seleção de ferramentas; opcionalmente, também pode usar um modelo de chat diferente. Isso separa responsabilidades e reduz a quantidade de ferramentas que o Agent principal precisa escolher diretamente, mas também acrescenta chamadas de modelo e tempo de espera. Conversas simples, com poucas ferramentas, geralmente não precisam de orquestração.

Esse recurso foi introduzido na versão 4.14.0 e ainda é considerado **experimental**. Esta página aborda a IA integrada do AstrBot. A orquestração fornecida por um aplicativo de IA externo deve ser configurada nesse próprio aplicativo.

## Como funciona

1. Quando o recurso está habilitado, o Agent principal recebe ferramentas chamadas `transfer_to_<name>`, como `transfer_to_research_assistant`, além das próprias ferramentas.
2. O Agent principal lê a descrição pública de cada SubAgent para decidir se deve delegar a tarefa. Ele envia uma tarefa clara e pode incluir imagens quando necessário.
3. O SubAgent usa o prompt, o diálogo predefinido e as ferramentas de sua Persona para concluir a tarefa.
4. O resultado é devolvido ao Agent principal, que organiza a resposta e continua a conversa.

O modelo decide quando delegar. A delegação não acontece automaticamente em todas as mensagens e também não segue um fluxo de trabalho fixo. Um SubAgent recebe a tarefa delegada e seu próprio diálogo predefinido; ele **não recebe automaticamente todo o histórico da conversa do Agent principal**. Inclua na tarefa o contexto necessário, os caminhos dos arquivos e as restrições relevantes.

A ferramenta de delegação também oferece suporte à execução em segundo plano. O Agent principal pode confirmar primeiro o envio da tarefa e ser reativado quando o SubAgent terminar. A entrega proativa ainda depende da plataforma de chat; consulte [Recursos proativos](/en/use/proactive-agent).

## Criar seu primeiro SubAgent {#configuration}

### 1. Preparar um modelo e uma Persona

Confirme se a IA integrada do AstrBot consegue conversar e se o modelo de chat oferece suporte a chamadas de ferramentas. Na WebUI, abra **Extensions → Persona** e crie uma Persona dedicada, por exemplo, “Assistente de pesquisa”:

- Explique como ela deve coletar informações, verificar fontes e apresentar resultados.
- Selecione apenas as ferramentas necessárias para a pesquisa, como a pesquisa na Web já configurada ou ferramentas MCP.
- Se ela apenas analisar textos, poderá ficar sem ferramentas.

A Persona descreve **como o assistente trabalha**. A descrição pública explica **em quais situações o Agent principal deve pedir sua ajuda**.

<span id="_2-create-a-subagent"></span>

### 2. Adicionar o SubAgent

Abra **Extensions → SubAgents**, clique em **Add SubAgent** e, em seguida, clique em **Expand** no novo cartão.

![Página de configuração de SubAgent (captura da interface em inglês)](/en/use/images/subagent-create-en.png)

| Configuração | O que informar |
| --- | --- |
| Agent name | Por exemplo, `research_assistant`. Comece com uma letra minúscula em inglês; use somente letras minúsculas, números e sublinhados. O limite é de 64 caracteres. Os nomes devem ser exclusivos. |
| Chat Provider (opcional) | Selecione o modelo de chat do SubAgent. Deixe vazio para usar o provedor de chat resolvido para a conversa atual. Este campo não é um campo separado para chave de API. |
| Choose Persona | Selecione a Persona que você criou. A prévia dela aparece à direita. Campo obrigatório. |
| Description for the main LLM | Descreva as tarefas adequadas, as informações de entrada necessárias e os resultados esperados. Evite descrições vagas, como “um assistente poderoso”. |
| Enable switch | Controla se este SubAgent participa da orquestração. Novos SubAgents são habilitados por padrão. |

Exemplo de descrição pública:

```text
Pesquisa e verifica informações. Delegue perguntas que exijam comparação, informações recentes ou resumo de fontes. Inclua a pergunta e as restrições. Retorno conclusões concisas com links para as fontes.
```

Gerencie as ferramentas na página **Persona**; a página do SubAgent não possui um seletor de ferramentas separado. Uma Persona com todas as ferramentas selecionadas pode usar as ferramentas disponíveis no momento. Uma seleção específica usa apenas as ferramentas correspondentes que ainda existem e estão habilitadas. As ferramentas de uso do computador também exigem o ambiente de execução e as permissões apropriados.

<span id="_1-enable-subagent-mode"></span>

### 3. Habilitar e salvar

Ative **Enable SubAgent orchestration** e clique em **Save**, no canto superior direito. Adicionar, editar, desabilitar ou excluir um SubAgent, assim como alterar qualquer uma das duas opções globais, exige salvar. Ao salvar, a orquestração é recarregada sem reiniciar o AstrBot.

Esta página gerencia **as configurações globais de orquestração**, não uma lista de SubAgents separada para o perfil de configuração selecionado.

## Remover ferramentas duplicadas do Agent principal

Por padrão, o Agent principal pode usar diretamente suas próprias ferramentas ou delegar tarefas. Quando **Deduplicate main LLM tools (hide tools duplicated by SubAgents)** está habilitado, as ferramentas sobrepostas atribuídas a SubAgents habilitados são removidas da lista de ferramentas do Agent principal.

Por exemplo, se ambos tiverem uma ferramenta de pesquisa, com a deduplicação desativada o Agent principal poderá pesquisar diretamente ou delegar a tarefa. Com a deduplicação ativada, ele usará o SubAgent de pesquisa para essa tarefa.

<span id="best-practices"></span>

Comece com a deduplicação desativada e habilite-a depois de confirmar que o SubAgent está funcionando. Dar todas as ferramentas a cada SubAgent dificulta a manutenção de responsabilidades claras.

## Verificar a configuração

1. Primeiro, confira as ferramentas necessárias: configure a pesquisa na Web, conecte o serviço MCP e assim por diante.
2. Envie uma solicitação explícita, como “Peça ao assistente de pesquisa para comparar estas duas opções e fornecer links para as fontes”.
3. Procure `transfer_to_research_assistant` e as chamadas seguintes na atividade de ferramentas da conversa ou em **Data & Logs → Logs**.
4. Antes de adicionar outros SubAgents, confirme se a resposta segue as instruções da Persona.

O modelo ainda pode responder diretamente. Criar um SubAgent, por si só, não garante que haverá delegação.

## Limitações e solução de problemas {#known-issues}

| Sintoma | O que verificar |
| --- | --- |
| Não é possível salvar | Confira os nomes, possíveis duplicatas e a seleção de Persona, inclusive nos SubAgents desabilitados. |
| O Agent principal nunca delega | Confira as duas opções de habilitação e se as configurações foram salvas. Use um modelo compatível com ferramentas e uma descrição pública específica. |
| O SubAgent não consegue usar uma ferramenta | Confira a seleção de ferramentas da Persona, o estado do plugin/MCP, o ambiente de execução e as permissões. Selecionar uma ferramenta desabilitada não a reativa. |
| O resultado não tem contexto | Especifique o contexto e as restrições que devem ser enviados. O histórico completo da conversa não é compartilhado automaticamente. |
| O modelo do SubAgent falha | Confira se o Chat Provider selecionado existe e funciona ou limpe o campo para usar o modelo da conversa. |
| As alterações da Persona não aparecem | Salve novamente a página do SubAgent para recarregar o conteúdo da Persona. |

Um SubAgent não é um contêiner separado nem uma fronteira independente de permissões da conta. Ele chama ferramentas no ambiente do AstrBot usado pela conversa atual. Configure o isolamento de arquivos e de execução em [Agent Sandbox](/pt-BR/use/astrbot-agent-sandbox).

O histórico de execução de um SubAgent não é salvo como uma conversa independente. Não há uma configuração separada de isolamento de Skills. Esta página não configura delegação em vários níveis e não deve ser tratada como uma árvore de Agents com aninhamento arbitrário.
