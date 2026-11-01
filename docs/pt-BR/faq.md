# Perguntas frequentes

## Sobre o painel

### Erro 404 ao abrir o painel

Baixe o arquivo `AstrBot-vxxxxx-dashboard.zip` na página de [releases](https://github.com/AstrBotDevs/AstrBot/releases), extraia o conteúdo e mova-o para `AstrBot/data`. Se o problema continuar, tente reiniciar o computador (conforme relatos da comunidade).

### Conta do primeiro acesso e senha aleatória

Na primeira inicialização, a conta da WebUI é `astrbot` por padrão. A senha inicial é gerada aleatoriamente; ela não é um valor fixo definido no código. Consulte os logs de inicialização e entre usando a senha inicial exibida:

```text
[00:27:40.590] [Core] [INFO] [dashboard.server:523]:
 ✨✨✨
  AstrBot v4.24.3 WebUI is ready

   ➜  Local: http://localhost:6185
   ➜  Initial username: astrbot
   ➜  Initial password: UiYVpZxnW8k22IWqf0ru5pOy
   ➜  Change it after logging in
 ✨✨✨
Set dashboard.host in data/cmd_config.json to enable remote access.
```

`UiYVpZxnW8k22IWqf0ru5pOy` é a senha padrão.

### Esqueci a senha do painel

Se você esqueceu a senha do painel do AstrBot, escolha o método de redefinição correspondente à forma como o programa foi implantado.

#### Implantação com Docker

A imagem já inclui a CLI do AstrBot, então você pode redefinir a senha dentro do contêiner:

```bash
sudo docker exec -it astrbot astrbot password
sudo docker restart astrbot # a nova senha entra em vigor após a reinicialização
```

O primeiro `astrbot` é o nome do contêiner. Substitua-o pelo nome real do seu contêiner (confira com `sudo docker ps`).

Para alterar também o nome de usuário, acrescente a opção `--username`: `sudo docker exec -it astrbot astrbot password --username <new-username>`.

#### Implantação por pacote uv / pip

Execute o comando abaixo no diretório de trabalho do AstrBot (aquele inicializado com `astrbot init`):

```bash
astrbot password
```

Para alterar também o nome de usuário, acrescente a opção `--username`: `astrbot password --username <new-username>`.

Em seguida, reinicie o AstrBot para que a alteração entre em vigor.

#### Outros métodos de implantação

Em implantações sem uma CLI disponível (como instalações a partir do código-fonte ou por painéis de gerenciamento), você pode editar diretamente o arquivo de configuração. Localize o campo `"dashboard"` em `AstrBot/data/cmd_config.json`. Por exemplo:

```json
  "dashboard": {
    "enable": true,
    "username": "astrbot",
    "password": "81e0c3dxxxxxxxxxxx78862e78",
    "pbkdf2_password": "pbkdf2_sha256$600000$1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "password_storage_upgraded": true,
    "password_change_required": true,
    "jwt_secret": "5e1b0280bcxxxxxxxxxxxxxxxxf4a",
    "host": "127.0.0.1",
    "port": 6185,
    "disable_access_log": true,
    "ssl": {
      "enable": false,
      "cert_file": "",
      "key_file": "",
      "ca_certs": ""
    }
  },
```

Exclua os campos `username`, `password`, `pbkdf2_password`, `password_storage_upgraded`, `password_change_required` e `jwt_secret`, incluindo seus valores, e salve o arquivo.

O trecho deverá ficar assim:

```json
  "dashboard": {
    "enable": true,
    "host": "127.0.0.1",
    "port": 6185,
    "disable_access_log": true,
    "ssl": {
      "enable": false,
      "cert_file": "",
      "key_file": "",
      "ca_certs": ""
    }
  },
```

Após a reinicialização, o AstrBot gerará automaticamente uma senha aleatória para o nome de usuário fixo `astrbot`. Consulte os logs de inicialização.

### A senha está correta, mas não consigo entrar após atualizar o AstrBot

Se você tem certeza de que a senha do painel está correta, mas ainda não consegue entrar após atualizar o AstrBot, os arquivos estáticos antigos da WebUI podem ser incompatíveis com a versão mais recente do backend.

Solução:

1. Pare o AstrBot.
2. Exclua a pasta `dist` dentro do diretório `data` do AstrBot: `AstrBot/data/dist`.
3. Inicie o AstrBot novamente.
4. Acesse o painel pelo navegador e force a atualização da página com `Ctrl+Shift+R` ou `Ctrl+F5` (ou `Cmd+Shift+R` no macOS).

Após a reinicialização, o AstrBot carregará ou baixará os arquivos da WebUI compatíveis com a versão atual.

## Sobre o núcleo do bot

### Como permitir que o AstrBot controle meu computador com macOS, Windows ou Linux?

1. Na WebUI do AstrBot, abra `Config`, selecione o perfil usado pelo seu bot e acesse `AI → Capabilities → Agent Computer Use`. Defina `Computer Use Runtime` como `local`. Esta seção requer o Agent Runner de IA integrado do AstrBot.
2. No mesmo perfil, acesse `Access Control → Administrators → Administrator IDs` e adicione seu ID de usuário (disponível pelo comando `/sid`).
3. Clique em `Save Configuration` no canto inferior direito.

> [!TIP]
> Por motivos de segurança, quando o ambiente de execução está definido como `local`, por padrão o AstrBot permite que apenas administradores do próprio AstrBot utilizem os recursos de controle do computador.
> Você pode selecionar `sandbox` como ambiente de execução para permitir que todos os usuários utilizem esses recursos em um ambiente isolado. Para saber mais, consulte [Ambiente sandbox do AstrBot](/en/use/astrbot-agent-sandbox.md).

### O bot não conversa em grupos

1. Em conversas de grupo, para evitar o excesso de mensagens, o bot não responde a todas as mensagens monitoradas. Tente mencionar o bot (@) ou usar uma palavra de ativação para iniciar a conversa, como o padrão `/`. Exemplo: `/hello`.

### Não tenho permissão para executar comandos de administrador

1. Os comandos administrativos padrão são `/name, /provider, /dashboard_update, /op, /deop, /persona, /llm, /plugin, /model, /groupnew`. Use o comando `/sid` para obter o ID de um usuário. Em seguida, abra `Config`, selecione o perfil usado pelo bot, adicione o ID em `Access Control → Administrators → Administrator IDs` e clique em `Save Configuration` no canto inferior direito.

### Caracteres chineses aparecem corrompidos ao renderizar imagens Markdown localmente (t2i)

Você pode personalizar a fonte. Consulte os detalhes em [#957](https://github.com/AstrBotDevs/AstrBot/issues/957#issuecomment-2749981802).

Fonte recomendada: [Maple Mono](https://github.com/subframe7536/maple-font).

### Não é possível interpretar a conclusão retornada pela API e o LLM retorna `<empty content>`

Isso acontece porque a API do provedor retornou um texto vazio. Tente as seguintes etapas:

1. Verifique se a API key ainda é válida.
2. Confira se o limite de chamadas ou a cota da API foi atingido.
3. Verifique a conexão de rede.
4. Tente redefinir.
5. Reduza a quantidade máxima de mensagens da conversa.
6. Troque para outro modelo do mesmo provedor ou para um provedor diferente.

## Sobre plugins

### Não consigo instalar um plugin

Os plugins são instalados pelo GitHub. O acesso ao GitHub pode ser instável em algumas redes. Configure e salve um proxy em `Settings → Network → Proxy & Dependency Sources → HTTP Proxy`. Na mesma página, você também pode definir um `GitHub Proxy Address` ou baixar o arquivo compactado do plugin e instalá-lo pela página de Plugins.

### Erro `No module named 'xxx'` após instalar um plugin

![imagem](https://files.astrbot.app/docs/source/images/faq/image.png)

Isso acontece porque as dependências do plugin não foram instaladas corretamente. Normalmente, o AstrBot instala automaticamente as dependências após a instalação do plugin, mas isso pode falhar nas seguintes situações:

1. Problemas de rede que impedem o download das dependências.
2. O autor do plugin não incluiu um arquivo `requirements.txt`.
3. Incompatibilidade com a versão do Python.

Solução:

Com base na mensagem de erro, consulte o README do plugin para instalar manualmente as dependências. Você pode instalar pacotes pela WebUI do AstrBot em `Data & Logs → Logs → Install pip Package`.

Digite o nome do pacote na janela, informe opcionalmente a URL de um repositório PyPI e clique em `Install`.

Se o autor do plugin não tiver incluído um arquivo `requirements.txt`, abra uma Issue no repositório do plugin solicitando que ele o adicione.
