# Configurar parâmetros personalizados do modelo

Você pode configurar os parâmetros do modelo pela WebUI:

1. Abra `Provedores` e selecione o provedor que contém seu modelo.
2. Na lista de modelos configurados, clique no nome do modelo ou no ícone de configurações para abrir a janela de configuração.
3. Em `Parâmetros personalizados do corpo da requisição` (`custom_extra_body`), adicione os parâmetros exigidos pelo modelo, como `temperature`, `top_p` ou `max_tokens`.
4. Clique em `Salvar`.

Os campos disponíveis dependem do provedor. Por exemplo, o Gemini expõe suas próprias configurações de geração em vez do campo genérico `custom_extra_body`. Consulte a documentação do seu provedor para saber quais parâmetros e valores são aceitos.
