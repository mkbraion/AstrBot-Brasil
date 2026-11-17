# Implantar o AstrBot na Compshare

A Compshare é uma plataforma da UCloud para aluguel de recursos de computação com GPU e APIs de LLM, oferecendo infraestrutura para IA, aprendizado profundo e cargas de trabalho científicas.

O AstrBot disponibiliza na Compshare uma imagem de implantação em um clique com Ollama + AstrBot e também oferece suporte às APIs de modelos da própria Compshare.

## Usar a imagem Ollama + AstrBot de implantação em um clique

> Especificações padrão da imagem: RTX 3090 de 24 GB + Intel de 16 núcleos + 64 GB de RAM + disco de sistema de 200 GB. A cobrança é feita conforme o uso; acompanhe seu saldo.

1. Crie uma conta na Compshare por meio [deste link](https://passport.compshare.cn/register?referral_code=FV7DcGowN4hB5UuXKgpE74).
2. Abra a [página da imagem do AstrBot](https://www.compshare.cn/images/0oX7xoGrzfre) e crie uma instância.
3. Depois da implantação, abra o `JupyterLab` pelo [console](https://console.compshare.cn/light-gpu/console/resources).
4. No JupyterLab, crie um terminal e execute:

```bash
cd
./astrbot_booter.sh
```

Se a inicialização for concluída com sucesso, você verá uma saída semelhante a esta:

```txt
(py312) root@f8396035c96d:/workspace# cd
./astrbot_booter.sh
Starting AstrBot...
Starting ollama...
Both services started in the background.
```

Depois da inicialização, acesse `http://<instance-public-ip>:6185` no navegador para abrir o painel do AstrBot.

O endereço IP público pode ser encontrado em **Console -> Basic Network (Public)**.

> Pode levar cerca de 30 segundos até que a página fique disponível.

Use a senha aleatória exibida nos logs de inicialização no primeiro acesso e o nome de usuário mostrado nos logs (geralmente `astrbot`). Altere a senha imediatamente após entrar.

Depois do login, você poderá redefinir a senha e continuar a configuração.

Por padrão, a instância importa o modelo `Ollama-DeepSeek-R1-32B`.

## Usar outros modelos

### Baixar modelos com Ollama

A imagem já inclui o Ollama. Você pode baixar qualquer modelo compatível e executá-lo localmente na instância.

1. Escolha um modelo na [busca do Ollama](https://ollama.com/search).
2. Conecte-se ao terminal da instância por SSH (no Console da Compshare, acesse **Instance List -> Console Command and Password**).
3. Execute `ollama pull <model-name>` e aguarde a conclusão.
4. Abra **Provedores → Conclusão de chat**, selecione a fonte Ollama pré-configurada, clique em **Buscar lista de modelos** e clique no botão `+` ao lado do modelo baixado. Se não houver uma fonte configurada, clique em **Adicionar**, selecione `Ollama`, informe a URL do Ollama da instância e clique em **Salvar e buscar modelos**.

### Usar a API de modelos da Compshare

O AstrBot também permite acessar diretamente as APIs de modelos fornecidas pela Compshare.

1. Localize o modelo desejado no [Centro de modelos da Compshare](https://console.compshare.cn/light-gpu/model-center).
2. Acesse **Provedores → Conclusão de chat → Adicionar**, selecione `OpenAI Compatible`, informe sua chave de API da Compshare e defina a URL base da API como `https://api.modelverse.cn/v1`.
3. Clique em **Salvar e buscar modelos** e, em seguida, clique no botão `+` ao lado do modelo desejado. Se a API não retornar uma lista de modelos, clique em **Salvar configuração**, selecione **Modelo personalizado** e informe o ID exato do modelo fornecido pela Compshare.

### Testar

Clique em **Testar modelo** na configuração do modelo para verificar a conexão. Depois, abra **Configuração**, selecione o perfil usado pelo bot, escolha o novo modelo em **IA → Modelo → Modelo de chat** e clique em **Salvar configuração**.

Use o seletor de chat no cabeçalho da WebUI ou envie uma mensagem ao bot pela plataforma de mensagens conectada para testar a resposta.

## Conectar plataformas de mensagens

Consulte os guias de integração de plataformas na [documentação do AstrBot](https://docs.astrbot.app/pt-BR/what-is-astrbot.html). Na barra lateral, procure a seção **Plataformas de mensagens**.

- Lark: [Conectar ao Lark](https://docs.astrbot.app/pt-BR/platform/lark.html)
- LINE: [Conectar ao LINE](https://docs.astrbot.app/pt-BR/platform/line.html)
- DingTalk: [Conectar ao DingTalk](https://docs.astrbot.app/en/platform/dingtalk.html)
- WeCom: [Conectar ao WeCom](https://docs.astrbot.app/en/platform/wecom.html)
- Conta oficial do WeChat: [Conectar à conta oficial do WeChat](https://docs.astrbot.app/en/platform/weixin-official-account.html)
- Bot oficial do QQ: [Conectar à API oficial do QQ](https://docs.astrbot.app/en/platform/qqofficial/webhook.html)
- KOOK: [Conectar ao KOOK](https://docs.astrbot.app/en/platform/kook.html)
- Slack: [Conectar ao Slack](https://docs.astrbot.app/pt-BR/platform/slack.html)
- Discord: [Conectar ao Discord](https://docs.astrbot.app/pt-BR/platform/discord.html)
- Outras opções: [Documentação do AstrBot](https://docs.astrbot.app/pt-BR/what-is-astrbot.html)

## Mais recursos

Para conhecer outros recursos, consulte a [documentação do AstrBot](https://docs.astrbot.app/pt-BR/what-is-astrbot.html).
