# Compactação de contexto

À medida que uma conversa cresce, o AstrBot envia ao modelo mais mensagens anteriores e resultados de ferramentas. Esse material forma o **contexto** do modelo, consome sua janela de contexto e aumenta a quantidade de tokens de entrada.

A compactação de contexto reduz o conteúdo mais antigo para que a conversa possa continuar. O AstrBot pode remover turnos anteriores ou solicitar a um modelo que os resuma. Essas configurações se aplicam à **IA integrada do AstrBot**; modos de execução de terceiros, como Dify e Coze, gerenciam o contexto em suas próprias plataformas.

> [!NOTE]
> A compactação ajuda em conversas longas, mas não consegue preservar todos os detalhes. Armazene materiais de referência de longo prazo em uma [base de conhecimento](/pt-BR/use/knowledge-base.md) ou em arquivos, em vez de depender apenas do histórico do chat.

## Configuração rápida

1. Abra **Config** na barra lateral da WebUI e selecione o perfil utilizado pelo seu bot.
2. Acesse **AI → Advanced → Context Management Strategy**. Se essa seção não aparecer, confirme que você está usando a IA integrada do AstrBot e que **Enable AI** está ativado. Consulte [Modo de execução de agentes](/pt-BR/use/agent-runner.md) para saber como trocar de modo.
3. Escolha uma estratégia em **Handling for History Limits or Context Window Pressure**. Novos perfis usam **Compress by LLM** por padrão.
4. Para começar, mantenha a proporção de contexto recente em `0.15` e deixe o modelo de compactação vazio para usar o modelo de chat atual. Mantenha **Max Turns Before Compression** em `-1` para evitar um limite adicional baseado na quantidade de turnos.
5. Clique em **Save Configuration**, no canto inferior direito.

![Configurações de gerenciamento de contexto]( /en/use/images/context-compress-settings-en.png )

Essas configurações pertencem ao perfil selecionado. Se seus bots usam perfis diferentes, confira cada perfil separadamente.

## Duas estratégias {#compression-strategies}

| Estratégia | O que acontece com o conteúdo mais antigo | Quando é indicada |
| --- | --- | --- |
| Truncate by Turns | Remove turnos anteriores sem gerar um resumo | Quando os assuntos anteriores não são mais necessários e se deseja reduzir latência e custo |
| Compress by LLM | Solicita a um modelo que resuma o conteúdo antigo e mantém parte do contexto recente sem alterações | Conversas longas ou tarefas de Agent que precisam continuar um trabalho ainda não concluído |

A compactação por LLM adiciona uma solicitação ao modelo, o que leva tempo e pode gerar custos. Os resumos podem omitir detalhes; já o truncamento descarta completamente o conteúdo removido.

### Configurações da compactação por LLM

| Configuração | Significado e recomendação |
| --- | --- |
| Model Provider ID for Context Compression | Deixe vazio para usar o modelo de chat da sessão atual ou selecione um modelo de chat já configurado. A janela de contexto desse modelo precisa ser grande o suficiente para o material que será resumido. |
| Recent Context Token Ratio to Keep | O padrão é `0.15`: um orçamento equivalente a 15% dos tokens do contexto atual é usado para manter o conteúdo recente sem alterações. O intervalo permitido é `0–0.3`. O AstrBot mantém turnos inteiros, em vez de cortar o conteúdo em um limite exato de tokens; uma proporção maior que zero preserva pelo menos o turno mais recente. |
| Context Compression Instruction | Deixe vazio para usar o prompt padrão. Um prompt personalizado pode pedir que o resumo preserve o objetivo da tarefa, as etapas concluídas, as principais conclusões, os caminhos de arquivos e as próximas ações. |

O resumo padrão prioriza o objetivo do usuário, o andamento da tarefa, as conclusões, os resultados úteis das ferramentas e os materiais já consultados, para que o trabalho possa continuar. Se o modelo escolhido para compactação estiver indisponível, o AstrBot tentará usar o modelo de chat atual. Se não conseguir gerar um resumo, recorrerá à remoção dos turnos mais antigos.

## Quando o contexto é processado

### 1. Uma solicitação se aproxima do limite de contexto do modelo

O AstrBot verifica o contexto **antes de cada solicitação ao modelo**, inclusive nas solicitações de acompanhamento feitas depois que um Agent chama ferramentas. A estratégia selecionada é acionada quando o uso do contexto ultrapassa aproximadamente **82%** da janela de contexto do modelo.

Depois do processamento, o AstrBot verifica o contexto novamente. Se ele ainda estiver longo demais, remove turnos completos, começando pelos mais antigos e mantendo o turno mais recente. As chamadas de ferramentas e seus resultados são tratados em conjunto para evitar registros de chamadas incompletos.

Se apenas o turno mais recente já for grande demais, a compactação automática ainda poderá não conseguir encaixar a solicitação na janela do modelo. Reduza o tamanho da entrada ou da saída da ferramenta, ou escolha um modelo com uma janela de contexto maior.

### 2. Um limite de turnos configurado é atingido

**Max Turns Before Compression** adiciona um limite ao tamanho do histórico. O valor padrão, `-1`, significa que não há limite baseado na quantidade de turnos. Com um valor positivo, o AstrBot também trunca o conteúdo anterior para aplicar esse limite antes de verificar o uso de tokens. **Turns to Discard When Limit Exceeded** controla quantos turnos são removidos de cada vez; o padrão é `1`.

Para priorizar o resumo das informações antigas em vez de removê-las antecipadamente por limite de turnos, mantenha o limite em `-1` e use a compactação por LLM. O valor `-1` não desativa a compactação automática baseada em tokens.

## Configure corretamente a janela de contexto do modelo {#️-important-model-context-window-settings}

A compactação depende da janela de contexto real do modelo de chat. Um valor muito alto pode permitir que as solicitações falhem antes do início da compactação; um valor muito baixo faz com que a compactação seja acionada cedo demais.

1. Abra **Providers → Chat Completion**.
2. Selecione o provedor à esquerda e edite o modelo configurado à direita.
3. Defina **Model context window size** (`max_context_tokens`) com o tamanho de janela publicado pelo provedor e salve.

Consulte [Modelos de chat](/en/providers/llm.md) para configurar modelos.

Quando `max_context_tokens` é `0`, o AstrBot tenta localizar o ID do modelo nos metadados integrados do [MODELS.DEV](https://models.dev/). Se o modelo não for conhecido, utiliza **Fallback context window size**, cujo valor padrão é `128000`. Portanto, definir o valor como `0` não desativa a compactação nem garante o reconhecimento de nomes de modelos personalizados.

Para um modelo não reconhecido, informe um valor correto de `max_context_tokens` em vez de depender do valor alternativo padrão.

## Perguntas frequentes

### Por que alguns detalhes anteriores desapareceram após a compactação?

Um resumo não preserva cada palavra, e o truncamento remove completamente o conteúdo mais antigo. Você pode especificar as informações importantes na instrução de compactação, aumentar a proporção de contexto recente ou armazenar materiais de referência de longo prazo em uma base de conhecimento. Aumentar essa proporção deixa menos espaço disponível para liberar por meio da compactação.

### Por que a compactação ainda não começou?

Verifique se você editou e salvou o perfil utilizado pela sessão atual. Normalmente, a compactação baseada em tokens só começa quando o uso ultrapassa aproximadamente 82% da janela de contexto. Uma janela configurada com tamanho excessivo pode atrasar o acionamento.

### Por que continuo recebendo um erro de limite de contexto?

Confira os tamanhos das janelas de contexto do modelo de chat e do modelo de compactação. Uma única mensagem grande, um arquivo ou o resultado de uma ferramenta pode fazer com que o turno mais recente ultrapasse o limite sozinho. A compactação não descarta indefinidamente a tarefa atual; reduza o tamanho da entrada e tente novamente.

### Como começar uma conversa do zero?

Envie `/reset` para limpar o contexto da conversa atual ou `/new` para criar uma nova conversa. Consulte [Comandos integrados](/pt-BR/use/command.md) para conhecer os comandos e as configurações do prefixo de ativação.
