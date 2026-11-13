# Recursos proativos

Os recursos proativos permitem que o AstrBot execute tarefas em horários programados, sem esperar uma nova mensagem do usuário. Por exemplo: “Lembre-me de fazer uma pausa daqui a dez minutos” ou “Pesquise notícias de tecnologia todas as manhãs e envie um resumo para este grupo”. Quando a tarefa é acionada, o Agent segue as instruções, chama o modelo e as ferramentas disponíveis e tenta enviar os resultados à conversa de destino.

Isso não é monitoramento autônomo contínuo. Primeiro, crie uma tarefa e mantenha o AstrBot em execução. Pesquisa, acesso a arquivos e outros recursos precisam ser configurados separadamente. Introduzido na versão v4.14.0, este recurso ainda é **experimental**.

<span id="how-to-use"></span>

## Configure os pré-requisitos

1. Em **Configuração**, escolha o perfil usado pela conversa de destino. Abra **IA**, habilite a IA e selecione **IA integrada do AstrBot**.
2. Confirme se o modelo de chat está funcionando e oferece suporte à chamada de ferramentas.
3. Abra **IA → Recursos → Agent proativo**, habilite a opção e clique em **Salvar configuração**. Isso disponibiliza a ferramenta `future_task` para gerenciar tarefas pelo chat.
4. Em **Extensões → Tarefas futuras**, clique em **Plataformas compatíveis** para verificar se a plataforma que receberá as mensagens está configurada e oferece suporte a mensagens proativas.

![Configuração do Agent proativo](/en/use/images/proactive-agent-settings-en.png)

Cada perfil controla se o Agent de chat recebe a ferramenta de agendamento. **Desativar essa opção não exclui nem pausa as tarefas existentes.** Desative ou exclua essas tarefas na página Tarefas futuras.

## Crie tarefas pelo chat {#future-tasks-futuretask}

<span id="features"></span>

Na conversa privada ou em grupo que deverá receber o resultado, diga ao AstrBot:

~~~text
Lembre-me de fazer uma pausa daqui a dez minutos, apenas uma vez.
~~~

Para uma tarefa recorrente:

~~~text
Todos os dias às 9h, no fuso horário Asia/Shanghai, pesquise três notícias de tecnologia. Envie os títulos, resumos breves e links das fontes para este grupo.
~~~

O modelo chama `future_task` para criar um agendamento. Não confie apenas na resposta “OK, agendado”: abra Tarefas futuras e confira as instruções, o horário de execução, a próxima execução e o destino da entrega. Uma tarefa de notícias também exige a [Pesquisa na Web](./websearch.md).

Você também pode pedir:

- “Liste as tarefas futuras que criei nesta conversa.”
- “Mude meu lembrete de pausa para amanhã às 15h.”
- “Exclua a tarefa de notícias que acabei de criar.”

A listagem, edição e exclusão pelo chat são limitadas às tarefas criadas **pelo remetente atual na conversa atual**. Os membros de um grupo não podem editar nem excluir as tarefas uns dos outros. Tarefas criadas pela WebUI não pertencem a um remetente do chat; os administradores devem gerenciá-las pela WebUI.

## Crie e gerencie tarefas pela WebUI

Abra **Extensões → Tarefas futuras** e clique em **Nova tarefa**. Não é necessário pedir ao modelo que crie a tarefa primeiro.

![Janela atual de criação de tarefa futura](/en/use/images/proactive-agent-task-en.png)

| Campo | Significado e exemplo |
| --- | --- |
| Nome da tarefa | Um nome fácil de reconhecer, como “Resumo diário de tecnologia”. |
| Requisitos da tarefa | Instruções que o Agent executará quando for acionado. Especifique as fontes, as etapas, o formato do resultado e se ele deve ser enviado. |
| Agendamento | Escolha entre execução única, intervalo, diária, semanal, mensal ou personalizada. |
| Entregar para (opcional) | Selecione uma conversa existente. Se deixar vazio, a tarefa poderá ser executada, mas os resultados não serão enviados automaticamente a um usuário ou grupo. |

Se nenhuma conversa aparecer, converse primeiro com o AstrBot na plataforma de destino e depois volte para selecioná-la. O destino é identificado por um UMO (origem unificada da mensagem), que inclui a plataforma, o tipo de mensagem e o identificador da conversa.

A lista mostra cada agendamento, o destino da entrega e a próxima execução. Pesquise por nome ou conteúdo, ou filtre pelo destino. Clique em uma tarefa para editá-la, use o interruptor para desativar a execução agendada e abra **Mais ações** para escolher **Executar agora** ou **Excluir**. Passe o cursor sobre as informações de horário para consultar a última execução e eventuais erros registrados.

- **Desativar** mantém a tarefa salva, mas pausa seus acionamentos agendados.
- **Executar agora** realmente executa a tarefa. Ela pode chamar modelos pagos ou serviços externos e enviar mensagens. Essa opção também funciona para tarefas desativadas.
- Executar manualmente uma tarefa de execução única não a exclui nem substitui sua execução agendada. Depois do teste, confira se ainda precisa manter o agendamento.
- Tarefas de execução única são excluídas após a tentativa de execução agendada, **mesmo quando a execução falha**. Tarefas recorrentes permanecem e continuam seguindo o agendamento.

## Agendamentos e fusos horários

Comece usando os seletores de horário diário ou semanal. Um agendamento personalizado utiliza uma expressão Cron de cinco campos:

~~~text
minuto hora dia-do-mês mês dia-da-semana
~~~

| Expressão | Significado |
| --- | --- |
| `0 9 * * *` | Todos os dias às 09h. |
| `0 17 * * fri` | Todas as sextas-feiras às 17h. |
| `0 9 1 * *` | No primeiro dia de cada mês às 09h. |

Os agendamentos recorrentes usam o fuso horário da tarefa. Novas tarefas criadas pela WebUI usam, por padrão, o fuso horário configurado para a conversa de destino ou, se ele não estiver definido, o fuso horário do sistema. O seletor de data e hora para tarefas de execução única usa o horário local do navegador e o converte em um registro de data e hora absoluto. Confira o agendamento resultante quando os fusos horários do navegador, do servidor e do contêiner forem diferentes.

Atualmente, o seletor de intervalo cria etapas de calendário Cron, e não um temporizador contado a partir do momento da criação. Por exemplo, uma tarefa configurada para executar a cada duas horas será executada nas horas pares. Os intervalos dos campos minuto, hora e dia têm limites de 59, 23 e 31, respectivamente; intervalos de dias que atravessam meses não representam uma duração fixa. Tarefas mensais marcadas para os dias 29, 30 ou 31 não são executadas nos meses que não possuem essa data.

O AstrBot precisa estar online para executar as tarefas. Os agendamentos salvos são carregados novamente após uma reinicialização, mas não conte com a reprodução de todos os lembretes que perderam o horário durante a indisponibilidade. Comece com uma tarefa de execução única programada para alguns minutos à frente, a fim de verificar o horário e a entrega.

## O que uma tarefa agendada pode utilizar

As tarefas usam a configuração e o contexto da conversa de destino. Alterações posteriores nos modelos, nas Personas e nas ferramentas podem afetar as próximas execuções. Inclua os detalhes necessários nas instruções da tarefa, em vez de escrever apenas “faça o que conversamos”. Tarefas sem destino de entrega usam uma conversa de agendamento separada e a configuração padrão.

O agendamento não concede recursos adicionais:

- Para obter informações atuais, configure a [Pesquisa na Web](./websearch.md).
- Para operações com arquivos ou execução de código, configure o [Agent Sandbox](./astrbot-agent-sandbox.md).
- Para serviços de terceiros, configure o [plugin](./plugin.md) correspondente ou o [MCP](./mcp.md).

### Plataformas compatíveis

Execução e entrega são etapas distintas. Uma execução bem-sucedida não garante que a plataforma aceitará a mensagem. Permissões da plataforma, identificadores de conversa, estado da conexão, janelas permitidas para mensagens proativas e formatos de mídia afetam a entrega. Consulte **Plataformas compatíveis** na página e a documentação da sua plataforma; uma lista fixa e antiga de plataformas não é uma referência completa de compatibilidade.

## Envio de mensagens multimídia

<span id="features-1"></span>

O AstrBot inclui a ferramenta `send_message_to_user`, que permite enviar texto, imagens, gravações de voz, vídeos, arquivos e menções. O Agent pode utilizá-la para enviar conteúdo que gerou ou recuperou, inclusive resultados de tarefas agendadas.

A ferramenta, por si só, não gera imagens nem áudio. A geração exige o modelo ou a ferramenta apropriada. Os arquivos precisam estar acessíveis ao Agent, e os tipos de mídia aceitos dependem da plataforma.

## Verificação e solução de problemas

Crie uma tarefa de execução única para alguns minutos à frente, solicitando o envio de um lembrete curto de teste. Confirme se ela aparece na lista, verifique o horário e mantenha o AstrBot em execução até a entrega. Teste tarefas complexas em uma conversa comum antes de agendá-las.

| Problema | O que verificar |
| --- | --- |
| O Agent diz que a tarefa foi agendada, mas a lista está vazia | Confira o perfil da conversa, a opção Agent proativo, se o modelo aceita chamadas de ferramentas e se `future_task` foi realmente chamada. |
| A tarefa está programada para o horário errado | Confira os fusos horários do perfil, do servidor/contêiner e do navegador; depois, verifique a próxima execução exibida. |
| Nada é executado no horário agendado | Confira o interruptor da tarefa, o tempo de atividade do AstrBot, o modelo e os serviços. Procure erros em **Dados e registros → Registros**. |
| A tarefa foi executada, mas a mensagem não chegou | Confira o destino da entrega, o suporte da plataforma, a conexão e as permissões de envio. Sem destino, não há entrega automática. |
| A pesquisa ou as operações com arquivos falham | Teste separadamente a configuração, as dependências e as permissões dessas ferramentas. O agendamento apenas desperta o Agent. |
| Uma tarefa de execução única desapareceu | Ela é excluída após a tentativa de execução agendada, mesmo em caso de falha. Consulte os registros para verificar o resultado. |
| O chat não encontra uma tarefa existente | Faça a consulta como o remetente original e na conversa original. Use a WebUI para tarefas criadas por outras pessoas ou pelo painel. |
