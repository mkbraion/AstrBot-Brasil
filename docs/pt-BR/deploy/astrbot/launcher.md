# Implantar o AstrBot com o AstrBot Launcher

## Método recomendado 1: AstrBot One-Click Launcher

O AstrBot One-Click Launcher oferece suporte a Windows, macOS e Linux.

0. Acesse [AstrBotDevs/astrbot-launcher](https://github.com/AstrBotDevs/astrbot-launcher).
1. **Opcional, mas recomendado:** adicione uma [**estrela ⭐**](https://github.com/AstrBotDevs/astrbot-launcher) ao projeto. Seu apoio ajuda os mantenedores a continuar aprimorando a ferramenta.
2. Localize **Releases** à direita, abra a versão mais recente e, em **Assets**, baixe o instalador correspondente ao seu sistema.

Por exemplo:

- Usuários de Windows x86: `AstrBot.Launcher_0.2.1_x64-setup.exe`
- Usuários de Windows em ARM: `AstrBot.Launcher_0.2.1_arm64-setup.exe`
- Usuários de macOS com Apple Silicon: `AstrBot.Launcher_0.2.1_aarch64.dmg`

No macOS, se aparecer a mensagem “está danificado e não pode ser aberto”, isso ocorre devido às restrições de segurança do sistema para aplicativos sem assinatura. Para corrigir:

1. Abra o Terminal.
2. Execute:
   `xattr -dr com.apple.quarantine /Applications/AstrBot\ Launcher.app`
3. Abra novamente o AstrBot Launcher.

## Método 2: instalador legado para Windows

Ainda recomendamos o One-Click Launcher acima, pois ele é mais simples, automatizado e adequado para a maioria dos usuários.

O instalador legado é um script do `PowerShell` muito pequeno (menos de 20 KB). Ele requer o `PowerShell`, que normalmente já vem incluído no `Windows 10` e em versões posteriores.

> [!WARNING]
> É necessário ter o `Python 3.12` ou posterior instalado e as variáveis de ambiente configuradas.

> [!TIP]
> Se a implantação falhar, tente usar Docker ou realizar a implantação manual.

## Baixar o instalador legado

Acesse <https://github.com/AstrBotDevs/AstrBotLauncher/releases/latest>.

Baixe o arquivo `Source code (zip)` e extraia seu conteúdo.

## Executar o instalador legado

> O vídeo pode estar desatualizado. Siga as etapas descritas aqui.

Depois de extrair os arquivos, abra a pasta.

Digite `PowerShell` na barra de endereço do Explorador de Arquivos e pressione Enter:

![Imagem](https://files.astrbot.app/docs/source/images/windows/image-4.png)

Arraste o arquivo `launcher_astrbot_en.bat` para a janela do PowerShell e pressione Enter.

> [!WARNING]
> - O script é seguro. Se o Windows exibir a mensagem `O Windows protegeu seu computador`, clique em `Mais informações` e depois em `Executar assim mesmo`.
> - Por padrão, o script usa `python`. Para indicar outro caminho ou comando do interpretador, edite `launcher_astrbot_en.bat`, localize `set PYTHON_CMD=python` e substitua `python` pelo seu próprio comando ou caminho.

Se o Python não for detectado, o script será encerrado e exibirá uma solicitação de correção.

O script verifica se existe uma pasta `AstrBot`. Caso não exista, baixa o código-fonte mais recente do AstrBot na página de [releases do GitHub](https://github.com/AstrBotDevs/AstrBot/releases/latest), instala as dependências e inicia o programa automaticamente.

## Concluído

Se tudo funcionar corretamente, os logs do AstrBot serão exibidos.

Se não houver erros, você verá uma mensagem semelhante a `🌈 Management panel started, accessible at`, acompanhada de vários endereços. Abra um deles para acessar a WebUI do AstrBot.

> [!TIP]
> No primeiro acesso, use a senha aleatória gerada durante a inicialização e exibida nos logs. Entre com essa senha e com o nome de usuário mostrado nos logs (geralmente `astrbot`) e altere a senha imediatamente.
>
> Se a WebUI retornar o erro 404:
> baixe o arquivo `dist.zip` na página de [releases](https://github.com/AstrBotDevs/AstrBot/releases), extraia seu conteúdo em `AstrBot/data` e, se necessário, reinicie o computador.

Em seguida, implante pelo menos um adaptador de plataforma de mensagens para começar a usar o AstrBot em aplicativos de mensagens instantâneas.

## Erro: o Python não está instalado

Se esse erro continuar aparecendo depois da instalação do Python e da reinicialização do computador, provavelmente o `PATH` está configurado incorretamente.

**Método 1**

Pesquise por Python no Windows e abra o local do arquivo:

![Imagem](https://files.astrbot.app/docs/source/images/windows/image.png)

Clique com o botão direito no atalho exibido e escolha abrir o local do arquivo:

![Imagem](https://files.astrbot.app/docs/source/images/windows/image-1.png)

Copie o caminho do arquivo:

![Imagem](https://files.astrbot.app/docs/source/images/windows/image-2.png)

Abra `launcher_astrbot_en.bat` no Bloco de Notas, localize `set PYTHON_CMD=python` e substitua `python` pelo comando ou caminho do seu interpretador. Mantenha as aspas se o caminho contiver espaços.

**Método 2**

Instale o Python novamente, marque a opção `Add Python to PATH` durante a instalação e reinicie o computador.
