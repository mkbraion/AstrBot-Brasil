# Conectar ao DeerFlow

A partir da versão v4.19.2, o AstrBot oferece suporte à conexão com o executor de agentes [DeerFlow](https://github.com/bytedance/deer-flow).

## Preparação: implantar o DeerFlow

Se você ainda não implantou o DeerFlow, siga a documentação oficial para concluir a instalação e a inicialização:

- [Repositório do DeerFlow no GitHub](https://github.com/bytedance/deer-flow)
- [Site oficial do DeerFlow](https://deerflow.tech/)
- [Guia de configuração do DeerFlow](https://github.com/bytedance/deer-flow/blob/main/backend/docs/CONFIGURATION.md)

Verifique se o DeerFlow está em execução e se o AstrBot consegue acessar o gateway do serviço. Por padrão, o endereço do gateway do DeerFlow é `http://127.0.0.1:2026`.

> [!TIP]
> - O campo `API Base URL` deve começar com `http://` ou `https://`.
> - Se o AstrBot e o DeerFlow estiverem em contêineres diferentes ou em hosts distintos, substitua `127.0.0.1` pelo endereço de rede local, nome de host ou domínio realmente acessível do serviço DeerFlow.

## Configurar o DeerFlow no AstrBot

Na WebUI, abra **Configurações**, selecione o perfil que deseja editar e acesse **IA**. Clique em **Mais ações** (`…`) ao lado do título, escolha **Alterar modo de execução** e selecione **DeerFlow**. Leia e marque a confirmação de redefinição e clique em **Usar este modo**. Verifique se **Ativar IA** está habilitado e preencha as configurações de conexão nesta página. A troca de modo redefine a configuração do modo atual; consulte [Modo de execução de agentes](/pt-BR/use/agent-runner).

Preencha os seguintes campos:

- `API Base URL`: endereço do gateway da API do DeerFlow. Padrão: `http://127.0.0.1:2026`
- `API Key`: opcional. Preencha se o gateway do DeerFlow estiver protegido por autenticação Bearer.
- `Authorization Header`: opcional. Valor personalizado do cabeçalho de autorização. Tem precedência sobre `API Key`.
- `Assistant ID`: corresponde a `assistant_id` do LangGraph. Padrão: `lead_agent`.
- `Model Name Override`: opcional. Substitui o modelo padrão configurado no DeerFlow.
- `Enable Thinking Mode`: define se o modo de raciocínio do DeerFlow será habilitado.
- `Enable Plan Mode`: corresponde a `is_plan_mode` do DeerFlow.
- `Enable Subagents`: corresponde a `subagent_enabled` do DeerFlow.
- `Maximum Concurrent Subagents`: corresponde a `max_concurrent_subagents`. Só tem efeito quando os subagentes estão habilitados. Padrão: `3`.
- `Recursion Limit`: corresponde a `recursion_limit` do LangGraph. Padrão: `1000`.

Depois de preencher as configurações, clique em **Salvar configuração**.

> [!TIP]
> - Se o DeerFlow já tiver um modelo padrão configurado, você pode deixar `Model Name Override` vazio.
> - Habilite as opções relacionadas a `plan mode` ou `subagent` somente quando os recursos correspondentes já estiverem configurados no próprio DeerFlow.

## Salvar a configuração

Quando todos os campos estiverem preenchidos, clique em **Salvar configuração**, no canto inferior direito. Esse perfil usará diretamente o modo de execução selecionado e as configurações de conexão informadas; não é necessário selecionar separadamente um provedor de executor nem um ID de provedor.

## Verificações comuns

Se as solicitações não estiverem sendo executadas corretamente pelo DeerFlow, verifique primeiro:

- se o serviço DeerFlow está em execução;
- se o ambiente do AstrBot consegue acessar o endereço informado em `API Base URL`;
- se as configurações de autenticação estão corretas;
- se o `Assistant ID` corresponde a um assistente realmente disponível no DeerFlow.
