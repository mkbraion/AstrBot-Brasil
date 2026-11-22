# Conectar ao AIHubMix

O [AIHubMix](https://aihubmix.com/?aff=4bfH) é um gateway de API de IA multimodelo que oferece acesso unificado a OpenAI, Claude, Gemini, DeepSeek, Kimi e outros serviços por meio de uma única chave de API. Além de LLMs, também oferece recursos de fala, embeddings, reclassificação e outras funcionalidades.

É totalmente compatível com o formato de API da OpenAI: basta alterar a URL base da API e a chave para começar. **Alguns modelos são totalmente gratuitos para desenvolvimento e testes.**

## Obter uma chave de API

1. Cadastre-se no [AIHubMix](https://aihubmix.com/?aff=4bfH).
2. Acesse **Console → Chaves de API** para criar uma nova chave.

![Obter uma chave de API](https://github.com/user-attachments/assets/d717f21b-2805-4aff-ac90-f5c98f17cb79)

## Configurar no AstrBot

Abra o painel do AstrBot e clique em **Provedores → Geração de respostas → Adicionar → OpenAI Compatible**.

Preencha os campos a seguir:

| Campo | Valor |
|-------|-------|
| URL base da API | `https://aihubmix.com/v1` |
| Chave de API | Sua chave do AIHubMix |

Informe o nome do provedor e a **Chave de API**, confira a **URL base da API** e clique em **Salvar e buscar modelos**. Clique em `+` ao lado do modelo desejado e confirme se ele está ativado. Como alternativa, clique em **Salvar configuração**, depois em **Modelo personalizado** e informe o ID exato do modelo. Use **Testar modelo**, ao lado do modelo configurado, para verificar se ele está disponível.

## Modelos recomendados

### Modelos gratuitos 🆓

Estes modelos são totalmente gratuitos e ótimos para desenvolvimento e testes:

| ID do modelo | Descrição |
|----------|-------------|
| `gpt-4.1-free` | Versão gratuita do GPT-4.1 |
| `gemini-3-flash-preview-free` | Versão gratuita do Gemini 3 Flash |
| `coding-glm-5-free` | Modelo de programação GLM-5, gratuito |
| `coding-minimax-m2.5-free` | Modelo MiniMax M2.5 para programação, gratuito |

### Modelos pagos (populares)

| ID do modelo | Provedor | Descrição |
|----------|----------|-------------|
| `gpt-5.4` | OpenAI | Modelo principal mais recente |
| `claude-sonnet-4-6` | Anthropic | Ótimo para raciocínio e programação |
| `gpt-5.3-chat-latest` | OpenAI | Chat de alto desempenho |
| `deepseek-v3.2` | DeepSeek | Boa relação entre custo e desempenho |
| `kimi-k2.5` | Moonshot | Contexto longo |
| `gemini-3.1-pro-preview` | Google | Multimodal |

> Consulte a lista completa de modelos na [documentação do AIHubMix](https://doc.aihubmix.com).

## Mais do que modelos de chat

O AIHubMix também oferece os recursos a seguir, todos configuráveis no AstrBot:

| Recurso | Local da configuração no AstrBot |
|------------|------------------------|
| Conversão de fala em texto (STT) | Provedores → Fala para texto → Adicionar |
| Conversão de texto em fala (TTS) | Provedores → Texto para fala → Adicionar |
| Embeddings | Provedores → Embedding → Adicionar |
| Reclassificação (Rerank) | Provedores → Rerank → Adicionar |

Adicione um provedor e selecione um modelo separadamente na guia de cada recurso. Você pode reutilizar a chave de API; configure o endpoint e os demais campos correspondentes a cada API.

## Definir como padrão

Abra **Configuração**, selecione o perfil que deseja usar e acesse **IA → Modelo**. Defina **Modelo de chat** como o modelo que acabou de adicionar e clique em **Salvar configuração**, no canto inferior direito. Essa configuração se aplica à IA integrada do AstrBot.
