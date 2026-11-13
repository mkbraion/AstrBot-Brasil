# Skills {#anthropic-skills}

Uma Skill é um manual de tarefas para um Agent. Ela reúne instruções, regras, modelos e materiais de referência em uma pasta cujo arquivo principal é `SKILL.md`. Também pode incluir scripts e exemplos.

Por exemplo, uma Skill de relatório semanal pode explicar como agrupar progresso, impedimentos e próximos passos em um formato consistente. Uma Skill de planilhas pode descrever a limpeza de dados e a geração de arquivos. O usuário descreve uma tarefa; o Agent verifica os nomes e as descrições das Skills, lê as instruções relevantes e carrega os recursos de apoio conforme necessário.

O AstrBot oferece suporte a esse formato de Agent Skills desde a versão v4.13.0. Ele não é exclusivo dos modelos Claude, mas o modelo precisa compreender as instruções. A leitura de arquivos, a chamada de ferramentas e a execução de scripts também exigem os recursos correspondentes.

## Diferenças entre Skills e ferramentas {#key-features}

| Tipo | O que oferece | Exemplo |
| --- | --- | --- |
| Ferramenta | Uma operação específica | Pesquisar na Web, ler um arquivo, executar Python |
| [MCP](./mcp.md) | Ferramentas de um serviço externo | Consultar calendários, pesquisar artigos científicos |
| Skill | Um fluxo de trabalho e recursos de apoio para uma tarefa | Escrever relatórios usando o modelo da equipe, analisar tabelas seguindo regras definidas |
| [Plugin](./plugin.md) | Extensões do AstrBot | Registrar comandos, processar mensagens e, opcionalmente, oferecer ferramentas ou Skills |

Primeiro, o AstrBot fornece ao Agent os nomes, as descrições e os caminhos dos arquivos das Skills. O Agent lê o conteúdo detalhado conforme necessário, em vez de carregar todos os arquivos no início. **Enviar uma Skill não instala as dependências de software nem concede permissões.** Configure separadamente os pacotes Python, as APIs e as ferramentas necessárias.

## Envie sua primeira Skill {#uploading-skills-to-astrbot}

1. Prepare um pacote de Skill em formato `.zip`, obtido de uma fonte confiável.
2. Abra `Extensões → Skills` na WebUI e clique no botão **+** no canto inferior direito. A antiga entrada independente de Skills agora fica no espaço de trabalho Extensões.
3. Selecione os arquivos ou arraste os arquivos ZIP para a janela. É possível enviar vários arquivos ZIP de uma só vez.
4. Clique em **Iniciar envio** e confira o resultado de cada arquivo. Volte à lista e confirme se a Skill instalada está habilitada.

![Janela de envio de Skills em lote](/en/use/images/skills-upload-en.png)

Arquivos com nomes duplicados na fila de envio são ignorados. O envio não substitui uma Skill local existente com o mesmo nome. Antes de atualizar, baixe uma cópia de segurança; depois, edite os arquivos locais ou exclua a Skill antiga e envie-a novamente.

### Estrutura do arquivo ZIP

Recomenda-se que o arquivo contenha uma ou mais pastas de Skills, cada uma com o arquivo `SKILL.md` diretamente em seu interior. Mantenha a capitalização do nome do arquivo:

~~~text
skills.zip
├── weekly-report/
│   ├── SKILL.md
│   └── references/
│       └── report-template.md
└── table-analysis/
    ├── SKILL.md
    └── scripts/
        └── analyze.py
~~~

Também é aceito um ZIP com `SKILL.md` diretamente na raiz. Para um pacote na raiz ou um arquivo que contenha apenas uma pasta de Skill, a WebUI usa o nome do arquivo ZIP, sem a extensão `.zip`, como identificador instalado. Para um pacote com várias Skills, usa o nome de cada pasta de Skill. Para evitar confusão, dê ao arquivo de uma Skill o mesmo nome da pasta, por exemplo, `weekly-report.zip`.

Use letras do alfabeto inglês, números, pontos, sublinhados ou hífens nos identificadores. Evite colocar as Skills dentro de uma pasta extra do repositório que não contenha um `SKILL.md`, e não basta renomear outro tipo de arquivo para `.zip`.

### Um arquivo SKILL.md mínimo

Este exemplo demonstra uma descrição e um fluxo de trabalho. O campo `description` deve informar **o que a Skill faz e quando deve ser usada**, para que o Agent possa decidir se deve carregá-la:

~~~markdown
---
name: weekly-report
description: Use when the user wants to turn scattered work notes into a weekly report with progress, blockers, and next steps.
---

# Weekly Report

1. Read the user's work notes; ask for any missing essential information.
2. Group completed work, ongoing work, and blockers.
3. Output sections named Progress, Issues and Risks, and Next Week.
4. Preserve dates, owners, and key figures. Do not invent progress.
~~~

Salve o arquivo como `weekly-report/SKILL.md`, compacte a pasta em `weekly-report.zip` e envie o pacote. Para consultar uma referência mais completa do formato, veja a [especificação Agent Skills](https://agentskills.io/specification) e a [documentação Claude Skills](https://code.claude.com/docs/en/skills).

## Configure o ambiente de execução e a Persona {#using-skills-in-astrbot}

### Dê ao Agent acesso aos arquivos das Skills

Abra **Configuração → IA → Recursos → Agent Computer Use**, escolha um ambiente de execução e salve:

- **Local:** o Agent usa as ferramentas de arquivos no ambiente de execução do AstrBot. Membros e administradores seguem políticas locais de permissão distintas. A leitura das instruções pode usar o acesso aos arquivos do espaço de trabalho sem executar código. A execução de scripts da Skill também exige permissão de execução e as respectivas dependências.
- **Sandbox:** o Agent lê arquivos e executa scripts em um ambiente separado. Configure primeiro a conexão com o sandbox. O AstrBot tenta sincronizar as Skills locais e as fornecidas por plugins com os sandboxes ativos.
- **Nenhum:** o inventário de Skills ainda pode ser enviado ao modelo, mas as ferramentas de leitura e execução do Agent Computer Use ficam indisponíveis. Não há garantia de que as instruções completas serão lidas, e os scripts das Skills não podem ser executados. Para usar Skills de forma prática, configure Local ou Sandbox.

Consulte [Agent Sandbox](./astrbot-agent-sandbox.md) para saber mais sobre escopos de arquivos, execução de código, rede e implantação. As Skills não contornam essas restrições nem concedem automaticamente aos membros comuns permissão para executar código.

### Selecione as Skills da Persona atual

1. Abra **Personas** e edite a Persona usada pela conversa.
2. Em **Recursos da Persona**, selecione as Skills. As Skills fornecidas por plugins são agrupadas por plugin; use o botão de engrenagem para selecionar Skills individualmente.
3. Salve a Persona e confirme se a conversa está usando-a. A Persona padrão utiliza todos os recursos disponíveis; use uma Persona personalizada para restringir a seleção.
4. Peça: “Use a Skill weekly-report para organizar estas anotações” e forneça as anotações. Você também pode descrever uma tarefa compatível e deixar que o Agent escolha a Skill.

Uma Skill pode estar indisponível porque foi desativada, porque seu plugin está desativado ou porque a Persona não a selecionou. Instalação, disponibilidade global, seleção pela Persona e permissões do ambiente de execução são configurações distintas.

## Gerencie as Skills instaladas

A lista em **Extensões → Skills** permite pesquisar por nomes, descrições e origens:

- **Habilitar / Desabilitar:** use o interruptor à direita. Desabilitar mantém os arquivos disponíveis para uso posterior.
- **Visualizar e editar:** clique em uma Skill local para abrir o editor de arquivos e consultar instruções, referências ou scripts. Arquivos de texto editáveis podem ser modificados e salvos.
- **Baixar:** exporte uma Skill local como ZIP para backup ou migração.
- **Excluir:** remova uma Skill local e seus arquivos. Use **Selecionar** para excluir várias de uma só vez.
- **Atualizar:** atualize a lista depois de modificar arquivos manualmente.

Skills fornecidas por plugins podem ser lidas, mas não podem ser editadas, baixadas nem excluídas nesta página; gerencie-as pelo plugin correspondente. Predefinições do sandbox não podem ser editadas, excluídas ou habilitadas/desabilitadas na página local de Skills. Essas restrições de origem não indicam uma falha de carregamento.

## Origens e prioridade das Skills

O AstrBot descobre Skills nos seguintes locais. Skills do espaço de trabalho ficam disponíveis para a solicitação atual, mas não aparecem na lista global de gerenciamento:

| Origem | Local ou método de descoberta | Gerenciamento |
| --- | --- | --- |
| Skills locais | Envios pela WebUI ou `data/skills/<skill_name>/SKILL.md` | Página Skills |
| Skills fornecidas por plugins | Diretório `skills/` de um plugin | Gerenciadas pelo plugin; também dependem da seleção de plugins no perfil de configuração atual |
| Predefinições do sandbox | Skills descobertas dentro do sandbox | Gerenciadas pelo sandbox; inicie pelo menos uma sessão de sandbox para preencher a descoberta |
| Skills do espaço de trabalho | `skills/<skill_name>/SKILL.md` dentro do espaço de trabalho da sessão atual | Descobertas por solicitação no ambiente Local; não aparecem na lista global de Skills |

O caminho de um espaço de trabalho geralmente é `data/workspaces/<normalized_umo>/skills/<skill_name>/SKILL.md`. O UMO identifica a sessão, e o nome do diretório é normalizado. No momento, as Skills do espaço de trabalho não são gravadas na configuração global nem sincronizadas automaticamente com sandboxes de terceiros.

Quando há nomes duplicados, a prioridade durante a solicitação é **Espaço de trabalho > Local > Plugin > Somente sandbox**. Uma substituição feita no espaço de trabalho se aplica apenas à solicitação atual.

A lista explícita de Skills de uma Persona filtra as Skills locais, de plugins e do sandbox, **mas não as Skills do espaço de trabalho**. Selecionar explicitamente nenhuma Skill também desabilita as Skills do espaço de trabalho. Quando uma Skill local é sincronizada com um sandbox, o AstrBot a trata como a mesma Skill e usa o caminho legível pelo sandbox nas solicitações executadas nele.

### Skills do Shipyard Neo

Quando o ambiente de execução é Sandbox e o driver é `shipyard_neo`, a página também oferece a opção **Skills locais / Neo Skills**. Neo Skills exibe candidatos e registros de versões, com ações de avaliação, promoção para `Canary` / `Stable`, sincronização e desativação/reversão.

Esse recurso gerencia versões reutilizáveis de Skills acumuladas no Neo. Ele não é necessário para enviar pacotes ZIP comuns. Comece pelo envio e pela execução local; consulte [Ambientes de sandbox de terceiros](/pt-BR/use/astrbot-agent-sandbox#third-party-sandbox-environment) para configurar a conexão com o Neo.

## Solução de problemas

| Sintoma | O que verificar |
| --- | --- |
| O envio não encontra `SKILL.md` | Use um ZIP válido, com o arquivo diretamente na raiz ou dentro de uma pasta de Skill; remova qualquer pasta extra que envolva o repositório |
| Já existe uma Skill com esse nome | O envio não a substitui; baixe uma cópia de segurança e edite-a ou exclua-a antes de enviar novamente |
| A lista não mostra uma descrição | Verifique se o frontmatter YAML inicial contém uma string no campo `description` |
| O Agent não usa a Skill | Mencione o nome explicitamente; confira o estado global, a Persona atual e a capacidade de leitura de arquivos |
| As instruções são carregadas, mas os scripts falham | Confira o ambiente de execução, as permissões de execução/rede do usuário e as dependências; uma Skill não instala dependências nem eleva permissões |
| Uma Skill de plugin está inativa ou restrita | Confira se o plugin está habilitado; os arquivos do plugin são gerenciados por ele |
| As predefinições do sandbox não aparecem | Inicie uma sessão de sandbox e atualize a lista; as predefinições vêm do cache de descoberta |
| As ações de edição/exclusão não estão disponíveis | Confira se é uma Skill local gerenciável, e não uma Skill de plugin ou uma predefinição do sandbox |

As Skills podem incluir scripts ou chamadas a serviços externos. Leia as instruções, confira as dependências e permissões e, em seguida, valide o resultado com uma tarefa pequena.
