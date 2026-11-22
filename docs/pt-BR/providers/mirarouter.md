# Conectar ao MiraRouter

O [MiraRouter](https://mirarouter.com/) oferece APIs estáveis e seguras compatíveis com a OpenAI para acessar modelos de IA populares usando uma única chave de API, centralizando o gerenciamento de chaves, uso e custos.

## Obter uma chave de API

1. Cadastre-se e entre na sua conta no [MiraRouter](https://mirarouter.com/).
2. Abra o console, crie uma chave de API e copie-a. A chave completa é exibida apenas uma vez; portanto, guarde-a em um local seguro.

## Configurar o AstrBot

Abra o painel do AstrBot e acesse **Provedores → Geração de respostas → Adicionar → MiraRouter**. Informe os valores a seguir:

| Campo | Valor |
| --- | --- |
| Nome do provedor | `MiraRouter` |
| URL base da API | `https://api.mirarouter.com/v1` |
| Chave de API | A chave de API criada no console do MiraRouter |

O AstrBot adiciona automaticamente o identificador `X-APP-CODE: astrbot` às solicitações enviadas ao MiraRouter.

Informe o nome do provedor e a **Chave de API**, confira a **URL base da API** e clique em **Salvar e buscar modelos**. Clique em `+` ao lado do modelo desejado e confirme se ele está ativado. Como alternativa, clique em **Salvar configuração**, depois em **Modelo personalizado** e informe o ID exato do modelo. Use **Testar modelo**, ao lado do modelo configurado, para verificar se ele está disponível.

## Definir como padrão

Abra **Configuração**, selecione o perfil que deseja usar e acesse **IA → Modelo**. Defina **Modelo de chat** como o modelo que acabou de adicionar e clique em **Salvar configuração**, no canto inferior direito. Essa configuração se aplica à IA integrada do AstrBot.

Para obter mais detalhes, consulte a [documentação do MiraRouter](https://docs.mirarouter.com/).
