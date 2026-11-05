# Conectando serviços de modelos

O AstrBot oferece suporte nativo aos formatos de API da OpenAI, Google GenAI e Anthropic. Você pode conectar qualquer provedor de serviços de modelos que seja compatível com um desses três formatos de API.

> [!NOTE]
> Se você estiver na China continental, recomendamos fortemente o uso de **provedores oficiais** ou de provedores em conformidade com as leis e regulamentações locais, por exemplo:
>
> - [MoonshotAI](https://moonshot.cn/)
> - [GLM](https://bigmodel.cn/)
> - [MiniMax](https://www.minimax.io/)
> - [Qwen](https://qwen.ai/apiplatform)
> - [DeepSeek](https://deepseek.com/)
>
> Esses provedores oferecem suporte ao formato de API da OpenAI. Consulte a documentação de cada serviço para encontrar a URL base da API e a chave de API; depois, informe esses dados nas configurações de provedores do AstrBot.
>
> O uso de serviços de modelos de terceiros que não estejam em conformidade com as normas aplicáveis pode trazer riscos de disponibilidade, privacidade ou natureza jurídica. Para obter detalhes, consulte o [EULA](https://github.com/AstrBotDevs/AstrBot/blob/master/EULA.md).

Você também pode conectar serviços de modelos oferecidos por (entre outros):

- Serviços oficiais de modelos da OpenAI ([OpenAI](https://openai.com/))
- Serviços oficiais de modelos da Anthropic ([Anthropic](https://www.anthropic.com/))
- Modelos Gemini do Google por meio do Google Cloud ([Google Cloud](https://cloud.google.com/))
- Serviços de modelos do OpenRouter ([OpenRouter](https://openrouter.ai/))

## Etapas de integração usando o DeepSeek como exemplo

Supondo que você já tenha criado uma conta e entrado no DeepSeek, siga estas etapas para conectar o serviço:

1. Acesse o console do DeepSeek: <https://platform.deepseek.com/>.
2. Clique no menu **API Keys** na barra lateral esquerda, crie uma nova chave de API e copie-a.
3. Clique no link **API Documentation**, próximo à parte inferior da barra lateral esquerda, para abrir a página da documentação da API.
4. Na documentação, localize a seção **OpenAI-compatible interface** e anote a URL base da API, por exemplo, `https://api.deepseek.com/v1`. Se o endereço não incluir `/v1`, acrescente esse sufixo.
5. No AstrBot, abra **Provedores → Geração de respostas**, clique em **Adicionar** e selecione `DeepSeek`. Para outros serviços compatíveis com o formato da API da OpenAI, selecione `OpenAI Compatible`. Informe o nome do provedor, a **Chave de API** e a **URL base**.
6. Clique em **Salvar e buscar modelos**. Localize o modelo desejado, clique em `+` e confirme que ele está ativado. Se não for possível carregar a lista de modelos, clique em **Salvar configuração**, depois em **Modelo personalizado** e informe o ID do modelo. Use **Testar modelo**, ao lado do modelo, para verificar a conectividade.
7. Abra **Configuração**, selecione o perfil que será usado e acesse **IA → Modelo**. Defina **Modelo de chat** como o modelo que acabou de adicionar e clique em **Salvar configuração**, no canto inferior direito. Essa configuração se aplica à IA integrada do AstrBot.

## Usando variáveis de ambiente para carregar chaves

> Recurso introduzido na v4.13.0.

Você pode usar variáveis de ambiente para carregar as chaves de API dos provedores. Na página de configuração do provedor, informe no campo **Chave de API** o nome da variável precedido por `$`, por exemplo: `$DEEPSEEK_API_KEY`.
