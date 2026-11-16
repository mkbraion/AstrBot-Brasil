# Implantar com o cliente desktop do AstrBot

O `AstrBot-desktop` foi desenvolvido para facilitar a implantação local do AstrBot em computadores pessoais. Ele oferece suporte a Windows, macOS e Linux.

Entre as diferentes opções de implantação, o cliente desktop é mais indicado para uso pessoal e local. Não é recomendado para operação contínua em servidores nem para ambientes de produção. Para implantações de produção, considere usar [Docker](/pt-BR/deploy/astrbot/docker) ou [Kubernetes](/pt-BR/deploy/astrbot/kubernetes).

Em comparação com soluções de linha de comando ou baseadas em contêineres, o cliente desktop oferece uma experiência gráfica pronta para uso, ideal para quem deseja começar sem precisar configurar manualmente o ambiente.

Repositório: [AstrBotDevs/AstrBot-desktop](https://github.com/AstrBotDevs/AstrBot-desktop)

## Para quem é indicado

- Pessoas que desejam uma implantação local rápida, com interface gráfica.
- Iniciantes que preferem não gerenciar manualmente ambientes Docker ou Python.
- Computadores pessoais que permanecem ligados e conectados, principalmente para uso diário individual ou por pequenas equipes.

## Principais recursos

- Instaladores para várias plataformas, prontos para uso após o download.
- Configuração por interface gráfica, reduzindo a complexidade da primeira implantação.
- Adequado para funcionar continuamente em um computador local.

## Download e instalação

1. Acesse a página de [releases do AstrBot-desktop](https://github.com/AstrBotDevs/AstrBot-desktop/releases).
2. Baixe o instalador correspondente ao seu sistema operacional (por exemplo, `.exe`, `.dmg`, `.rpm` ou `.deb`).
3. Depois da instalação, abra o cliente desktop e siga o assistente de configuração para concluir a inicialização.

## Diferenças em relação à implantação pelo Launcher

- **Cliente desktop:** prioriza uma experiência gráfica pronta para uso.
- **Launcher:** prioriza a inicialização automatizada por scripts, sendo adequado para quem prefere um fluxo de implantação tradicional.
- Consulte também [Implantar com o AstrBot Launcher](/pt-BR/deploy/astrbot/launcher).
