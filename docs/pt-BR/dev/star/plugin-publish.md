# Publicar plugins no marketplace

Depois de concluir o desenvolvimento do seu plugin, você pode publicá-lo no Marketplace de Plugins do AstrBot para que mais pessoas possam aproveitar seu trabalho.

O AstrBot usa o GitHub para hospedar os plugins. Portanto, será necessário enviar o código do plugin para o repositório GitHub que você criou anteriormente.

Para publicar, acesse a [página de publicação de plugins do AstrBot](https://cloud.astrbot.app/publish). É necessário registrar uma conta na AstrBot Cloud para realizar a publicação.

<!-- ![preencher o formulário](https://files.astrbot.app/docs/source/images/plugin-publish/image.png) -->

Abaixo está um exemplo completo de metadados de plugin (`metadata.yaml`), que será interpretado automaticamente pelo sistema:

```yaml
name: astrbot_plugin_example                 # Identificador do plugin, em inglês e exclusivo
display_name: Nome de exibição do plugin     # Nome apresentado aos usuários
# short_desc: Resumo do plugin em uma linha  # (Opcional) Descrição curta para a interface compacta
desc: Descrição detalhada dos recursos e do uso do plugin.  # Descrição detalhada do plugin
  Aceita texto em várias linhas com formatação Markdown.
version: 1.0.0                               # Versão do plugin (siga o versionamento semântico)
author: Nome do autor                        # Nome do autor
repo: https://github.com/your-name/repo      # URL do repositório do plugin
# astrbot_version: ">=4.17.0"                # (Opcional) Intervalo de versões do AstrBot
# support_platforms:                         # (Opcional) Lista de adaptadores de plataforma compatíveis
#   - aiocqhttp
#   - qq_official
# social_link: https://github.com/your-web   # (Opcional) Site pessoal, perfil do GitHub etc.
# tags:                                      # (Opcional) Tags para categorização e pesquisa no marketplace
  # - exemplo
```

[Adaptadores de plataforma compatíveis](plugin-new.md#declarar-as-plataformas-compatíveis-opcional)

::: warning Limite de tamanho
O arquivo ZIP do plugin enviado ao marketplace **não pode ultrapassar 16 MB**.

Se ultrapassar esse limite, o pipeline de CI/CD rejeitará automaticamente o envio.
::: details Para aumentar as chances de aprovação e publicação sem problemas, recomendamos:

- **Compacte os recursos estáticos**: comprima imagens, áudios e outros arquivos de recursos do plugin para reduzir o tamanho.
- **Remova arquivos desnecessários**: evite incluir diretórios como `.git`, `__pycache__`, `node_modules` ou arquivos de configuração de desenvolvimento no repositório do plugin. Adicione um arquivo `.gitignore` à raiz do repositório para excluí-los.
- **Otimize o tamanho das dependências**: se o plugin depender de bibliotecas grandes, considere reduzir o conjunto de dependências ou importar apenas o que for necessário.
- **Use `.gitattributes` ou uma branch de publicação**: reduza o tamanho do ZIP incluindo somente os arquivos necessários para distribuição.

Se, por requisitos do projeto, realmente não for possível reduzir o plugin para menos de 16 MB, entre em contato com o mantenedor para solicitar a liberação manual desse limite.
:::
