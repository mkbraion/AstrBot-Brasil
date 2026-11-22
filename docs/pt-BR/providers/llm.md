# Provedores de modelos de linguagem (LLM)

Na WebUI, abra **Provedores → Geração de respostas**, clique em **Adicionar** e selecione um tipo de provedor. Para um serviço compatível com a OpenAI, selecione `OpenAI Compatible` e informe a URL base da API e a chave de API fornecidas pelo serviço.

Informe o nome do provedor e a **Chave de API**, confira a **URL base da API** e clique em **Salvar e buscar modelos**. Clique em `+` ao lado do modelo desejado e confirme se ele está ativado. Como alternativa, clique em **Salvar configuração**, depois em **Modelo personalizado** e informe o ID exato do modelo. Use **Testar modelo**, ao lado do modelo configurado, para verificar se ele está disponível.

Abra **Configuração**, selecione o perfil que deseja usar e acesse **IA → Modelo**. Defina **Modelo de chat** como o modelo que acabou de adicionar e clique em **Salvar configuração**, no canto inferior direito. Essa configuração se aplica à IA integrada do AstrBot.

Consulte [Conectar serviços de modelos](./start.md) para ver as etapas detalhadas.

> As configurações de conexão dos provedores são armazenadas em `provider_sources`, em `data/cmd_config.json`; as configurações individuais dos modelos são armazenadas em `provider`.
