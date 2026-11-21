---
outline: deep
---

# Guia de desenvolvimento de plugins do AstrBot 🌠

Bem-vindo ao Guia de Desenvolvimento de Plugins do AstrBot! Esta seção orienta você durante a criação de plugins para o AstrBot. Antes de começar, recomendamos que você tenha os seguintes conhecimentos básicos:

1. Alguma experiência com programação em Python.
2. Alguma experiência com Git e GitHub.

## Configuração do ambiente

### Obter o modelo de plugin

1. Acesse o modelo de plugin do AstrBot: [helloworld](https://github.com/Soulter/helloworld).
2. Clique em `Use this template`, no canto superior direito.
3. Em seguida, clique em `Create new repository`.
4. Preencha o nome do plugin no campo `Repository name`. Convenções para nomear plugins:
   - Recomenda-se começar com `astrbot_plugin_`;
   - Não use espaços;
   - Use apenas letras minúsculas;
   - Prefira um nome curto e objetivo.
5. Clique em `Create repository`, no canto inferior direito.

### Clonar o projeto para a máquina local

Clone o projeto principal do AstrBot e o repositório do plugin que você acabou de criar para sua máquina local.

```bash
git clone https://github.com/AstrBotDevs/AstrBot
mkdir -p AstrBot/data/plugins
cd AstrBot/data/plugins
git clone <your-plugin-repository-url>
```

Em seguida, abra o projeto `AstrBot` no `VSCode`. Navegue até o diretório `data/plugins/<your-plugin-name>`.

Atualize o arquivo `metadata.yaml` com as informações de metadados do seu plugin.

> [!WARNING]
> Não deixe de modificar esse arquivo: o AstrBot depende de `metadata.yaml` para reconhecer os metadados do plugin.

### Definir o logotipo do plugin (opcional)

Você pode adicionar um arquivo `logo.png` ao diretório do plugin para usá-lo como logotipo. Mantenha a proporção de 1:1; o tamanho recomendado é 256 × 256 pixels.

![Exemplo de logotipo de plugin](https://files.astrbot.app/docs/source/images/plugin/plugin_logo.png)

### Nome de exibição do plugin (opcional)

Você pode modificar (ou adicionar) o campo `display_name` no arquivo `metadata.yaml` para definir o nome exibido do plugin em locais como o marketplace, facilitando a leitura pelos usuários.

Os nomes e as descrições dos plugins podem acompanhar o idioma da WebUI. Consulte [Internacionalização de plugins](/en/dev/star/guides/plugin-i18n).

### Descrição curta do plugin (opcional)

Você pode adicionar o campo `short_desc` ao `metadata.yaml`. Ele será exibido como descrição curta nos cartões do marketplace. Use uma frase objetiva. Se o campo não for informado, os cartões usarão o valor de `desc`.

```yaml
short_desc: A one-line summary of your plugin.
```

### Incluir Skills em um plugin (opcional)

Os plugins podem fornecer um diretório `skills/`. Depois que o AstrBot carregar o plugin, as Skills válidas desse diretório serão adicionadas automaticamente ao Gerenciador de Skills, com o plugin identificado como origem.

Para incluir várias Skills, use esta estrutura:

```text
your_plugin/
  metadata.yaml
  main.py
  skills/
    web-search-helper/
      SKILL.md
    report-writer/
      SKILL.md
```

Se o próprio diretório `skills/` corresponder a uma única Skill, você também poderá colocar o arquivo `SKILL.md` diretamente nele:

```text
your_plugin/
  skills/
    SKILL.md
```

Nesse caso, o nome da Skill será o nome do diretório do plugin. As Skills fornecidas por plugins são gerenciadas pelo próprio plugin e aparecem como fontes somente para leitura em `Extensões → Skills` na WebUI. Elas podem ser ativadas ou desativadas, mas não podem ser excluídas nem editadas em Skills locais. Quando o plugin for desinstalado ou atualizado, as Skills incluídas acompanharão os arquivos do plugin.

### Declarar as plataformas compatíveis (opcional)

Você pode adicionar o campo `support_platforms` (`list[str]`) ao `metadata.yaml` para declarar quais adaptadores de plataforma são compatíveis com seu plugin. A página do plugin na WebUI exibirá esse campo.

```yaml
support_platforms:
  - telegram
  - discord
```

Os valores de `support_platforms` devem ser chaves de `ADAPTER_NAME_2_TYPE`. Atualmente, são aceitos:

- `aiocqhttp`
- `qq_official`
- `qq_official_webhook`
- `telegram`
- `wecom`
- `wecom_ai_bot`
- `lark`
- `dingtalk`
- `discord`
- `slack`
- `kook`
- `vocechat`
- `weixin_official_account`
- `weixin_oc`
- `satori`
- `misskey`
- `line`
- `matrix`
- `mattermost`

### Declarar o intervalo de versões do AstrBot (opcional)

Você pode adicionar o campo `astrbot_version` ao `metadata.yaml` para declarar o intervalo de versões do AstrBot exigido pelo plugin. O formato segue os especificadores de dependência do `pyproject.toml` (PEP 440) e não deve incluir o prefixo `v`.

```yaml
astrbot_version: ">=4.16,<5"
```

Exemplos:

- `>=4.17.0`
- `>=4.16,<5`
- `~=4.17`

Se quiser declarar apenas uma versão mínima, use:

- `>=4.17.0`

Se a versão atual do AstrBot não atender a esse intervalo, o plugin será impedido de carregar e apresentará um erro de compatibilidade. Durante a instalação pela WebUI, você poderá selecionar `Ignore Warning and Install` para ignorar essa verificação.

### Depurar plugins

O AstrBot utiliza um mecanismo de injeção de plugins em tempo de execução. Por isso, para depurar plugins, é necessário iniciar a aplicação principal do AstrBot.

Você pode usar o recurso de recarregamento a quente do AstrBot para agilizar o processo de desenvolvimento.

Depois de modificar o código do plugin, abra `Extensões → Plugins` na WebUI do AstrBot, localize seu plugin e clique no ícone de atualização (`Reload Extension`) no cartão correspondente.

Se o plugin não carregar por causa de erros no código ou por outros motivos, clique no botão `Reload` na lista `Failed to Load Plugins` da mesma página.

### Gerenciar dependências do plugin

Atualmente, o AstrBot gerencia as dependências dos plugins usando o arquivo `requirements.txt` integrado ao pip. Se seu plugin precisar de bibliotecas de terceiros, crie um arquivo `requirements.txt` no diretório do plugin e liste nele as dependências utilizadas. Isso evita erros de módulo não encontrado quando os usuários instalarem o plugin.

> Para consultar o formato completo do `requirements.txt`, veja a [documentação oficial do pip](https://pip.pypa.io/en/stable/reference/requirements-file-format/).

## Princípios de desenvolvimento

Agradecemos por contribuir com o ecossistema do AstrBot. Ao desenvolver plugins, siga estes princípios, que também representam boas práticas de programação:

- Teste todas as funcionalidades.
- Inclua comentários abrangentes.
- Armazene dados persistentes no diretório `data`, e não no próprio diretório do plugin, para evitar perda de dados durante atualizações ou reinstalações.
- Implemente mecanismos robustos de tratamento de erros; um único erro não deve interromper o plugin.
- Antes de enviar suas alterações, use a ferramenta [ruff](https://docs.astral.sh/ruff/) para formatar o código.
- Não use a biblioteca `requests` para fazer requisições de rede; prefira bibliotecas assíncronas, como `aiohttp` ou `httpx`.
- Se estiver ampliando a funcionalidade de um plugin existente, priorize enviar um PR para esse plugin em vez de criar outro separado (a menos que o autor original tenha deixado de mantê-lo).
- Se seu plugin aproveitar o design, as ideias de funcionalidades ou a abordagem de implementação de outro projeto, reconheça claramente a inspiração no README e inclua um link para o projeto correspondente.
- Se você usar, modificar ou portar código ou recursos de outro projeto, respeite a licença de código aberto original e mantenha os avisos de direitos autorais e de licença exigidos por ela.
