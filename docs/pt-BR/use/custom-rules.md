# Regras personalizadas

As regras personalizadas permitem criar exceções para **uma sessão específica**, sem precisar duplicar um perfil de configuração inteiro para cada grupo ou conversa privada. Por exemplo:

- Definir uma persona profissional e um modelo de chat específico para um grupo de trabalho, enquanto as demais sessões mantêm suas configurações padrão.
- Permitir que um grupo use comandos de plugins sem receber respostas automáticas da IA.
- Desativar respostas por voz ou determinados plugins em uma conversa privada.
- Escolher bases de conhecimento específicas para uma sessão.

Essas regras têm prioridade sobre as configurações correspondentes do perfil da sessão. As configurações sem substituição continuam funcionando normalmente. As regras não criam modelos, personas, plugins ou bases de conhecimento; configure esses recursos primeiro nas respectivas páginas.

## Identifique a sessão (UMO)

UMO (*Unified Message Origin*, ou origem unificada da mensagem) identifica uma sessão específica em uma instância de plataforma. As regras personalizadas pertencem ao **UMO**, não ao nome de exibição do usuário nem ao título da conversa atual.

Envie `/sid` no grupo ou na conversa privada que deseja configurar e compare o UMO retornado com a sessão exibida na WebUI. Nomes semelhantes entre plataformas e conversas podem causar confusão; conferir o UMO ajuda a selecionar a origem correta. Consulte [Comandos integrados](/pt-BR/use/command.md) para obter detalhes sobre comandos e prefixos de ativação.

> [!NOTE]
> O isolamento de conversas por membro em grupos afeta a identificação das sessões. Use o UMO retornado pela mensagem de destino. Criar uma nova conversa dentro de uma sessão não remove as regras personalizadas associadas àquele UMO.

## Adicione sua primeira regra

1. Converse com o bot no grupo ou na conversa privada de destino para que o AstrBot registre a origem.
2. Abra **Custom Rules** na barra lateral da WebUI.
3. Clique em **Add Rule**, selecione o destino em **Select Session** e clique em **Next**. Se a sessão já tiver regras, use o botão de edição correspondente na lista.
4. Altere as configurações em **Edit Custom Rules**, por exemplo, o modelo de chat em **Provider Configuration**.
5. Clique em **Save** abaixo da seção alterada. As seções de serviço, provedor, persona, plugin e base de conhecimento são salvas separadamente. Salve cada seção modificada.
6. Envie uma nova mensagem na sessão de destino para conferir o resultado.

![Edição de regras personalizadas]( /en/use/images/custom-rules-edit-en.png )

As regras salvas entram em vigor sem reiniciar o AstrBot. Os antigos pontos de acesso **Session Management** e **More Features → Custom Rules** agora correspondem à opção **Custom Rules**, diretamente na barra lateral.

## Configurações disponíveis

| Seção | Configuração | Finalidade |
| --- | --- | --- |
| Service Configuration | Enable Session | Quando desativada, interrompe o processamento de mensagens dessa origem, incluindo respostas normais da IA e respostas de plugins. Reative-a pela WebUI. |
| Service Configuration | Enable LLM | Quando desativada, interrompe o processamento normal de conversas com IA para a sessão. Os comandos de plugins ainda podem funcionar; cada plugin controla seu próprio comportamento. |
| Service Configuration | Enable TTS | Controla se a sessão pode usar saída de fala sintetizada. Um modelo TTS e as configurações correspondentes do perfil já precisam estar configurados. |
| Service Configuration | Custom Name | Adiciona uma observação para ajudar a identificar a sessão sem alterar seu UMO. |
| Provider Configuration | Chat Provider, STT Provider, TTS Provider | Seleciona modelos configurados para essa sessão ou **Follow Config**. |
| Persona Configuration | Select Persona | Força uma persona para essa sessão. Deixar o campo vazio remove a regra de persona forçada. |
| Plugin Configuration | Disabled Plugins | Desativa os plugins selecionados nessa sessão, sem afetar as demais sessões. |
| Knowledge Base Configuration | Select Knowledge Bases, Top K Results | Substitui a seleção de bases de conhecimento do perfil e a quantidade de resultados de recuperação. |

Os controles de serviço determinam se a sessão pode utilizar recursos que já foram configurados. Marcar LLM ou TTS não ativa um recurso desabilitado no perfil nem configura automaticamente um modelo.

Consulte [WebUI](/pt-BR/use/webui.md), [Plugins](/en/use/plugin.md) e [Base de conhecimento](/pt-BR/use/knowledge-base.md) para configurar os recursos correspondentes de persona, plugins e bases de conhecimento.

## Regras e perfis de configuração

Um **perfil** configura um conjunto completo de comportamentos do bot, como modelos, condições de ativação, processamento de mensagens e ferramentas. Uma **regra personalizada** altera configurações selecionadas para uma sessão individual.

Por exemplo, dois grupos podem usar o perfil `default`, enquanto apenas o grupo A precisa de um modelo de chat diferente. Adicione uma regra de modelo ao grupo A sem afetar o grupo B. Se depois você alterar o modelo de chat no perfil `default`, o grupo A continuará usando sua substituição até que a regra seja removida ou que **Follow Config** seja selecionado.

Uma regra não consegue carregar um plugin que tenha sido desativado globalmente. Primeiro, habilite-o na página **Plugins**; depois, use as regras personalizadas para desativá-lo apenas nas sessões desejadas.

## Edite regras e restaure os padrões

Pesquise a sessão ou sua observação na lista e use o botão de edição. Cada seção possui seu próprio botão para salvar.

- **Modelos:** selecione **Follow Config** e salve para remover a substituição do modelo.
- **Persona:** limpe a seleção e salve para remover a regra de persona forçada e restaurar a seleção normal de persona.
- **Plugins:** remova um plugin da lista de desativados e salve. Limpar a lista remove a regra de desativação de plugins da sessão.
- **Bases de conhecimento:** limpe a seleção e salve para remover a regra da sessão e restaurar as configurações de base de conhecimento do perfil. **Isso não desativa as bases de conhecimento.**
- **Sessão inteira:** use o botão de exclusão na lista e confirme para remover todas as regras personalizadas daquele UMO.

Excluir regras não exclui modelos, plugins, bases de conhecimento nem o histórico do chat.

## Operações em lote e grupos

Use **Batch Operations**, abaixo da lista de regras, para alterar várias sessões:

1. Selecione sessões na lista ou escolha todas as sessões, todos os grupos, todas as conversas privadas ou um grupo personalizado em **Apply to**.
2. Selecione o estado de LLM ou TTS, ou o modelo de chat que deseja alterar.
3. Clique em **Apply Changes** e confira as sessões de destino.

Somente as configurações selecionadas serão alteradas. Comece com algumas sessões antes de aplicar mudanças a um conjunto maior.

**Group Management** permite organizar sessões relacionadas em um grupo com nome e usar esse grupo como escopo de uma operação em lote. Um grupo não faz com que seus membros herdem automaticamente regras compartilhadas; aplique as alterações em lote depois de adicionar os membros.

## Perguntas frequentes

### Minha sessão não aparece em Add Rule

Converse com o bot nessa sessão e, em seguida, atualize a página ou abra **Add Rule** novamente. Sessões que já possuem regras são excluídas da lista de adição; edite-as diretamente na lista principal.

### Por que uma sessão continua usando o modelo ou a persona antigos depois que altero o perfil?

Verifique se existem regras para aquele UMO. As substituições da sessão continuam tendo prioridade. Selecione **Follow Config**, limpe a persona forçada ou remova a regra e teste novamente.

### Desativei a sessão. Por que um comando não consegue reativá-la?

Desativar o processamento da sessão impede que suas mensagens cheguem às etapas posteriores de processamento. Reative a sessão pela WebUI, em vez de depender de comandos enviados no chat desativado.

### Uma alteração salva não produz efeito

Confira o UMO de destino, o resultado do salvamento da seção editada e a disponibilidade do recurso selecionado. Faça um teste com uma nova mensagem; as regras não alteram respostas que já foram geradas.
