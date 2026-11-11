# Interpretador de código baseado em Docker

> [!WARNING]
> Este recurso foi descontinuado. Consulte a documentação mais recente sobre o [Ambiente Agent Sandbox](/pt-BR/use/astrbot-agent-sandbox.md). O recurso deixará de estar disponível após a versão v4.12.0.

A partir da versão `v3.4.2`, o AstrBot oferece suporte a um interpretador de código para ampliar os recursos dos LLMs e permitir diversas operações automatizadas.

> [!TIP]
> Este recurso ainda está em fase experimental e pode apresentar problemas. Se encontrar alguma dificuldade, abra uma issue no [GitHub](https://github.com/AstrBotDevs/AstrBot/issues). Você também pode participar do nosso grupo de discussão: [322154837](https://qm.qq.com/cgi-bin/qm/qr?k=EYGsuUTfe00_iOu9JTXS7_TEpMkXOvwv&jump_from=webapi&authKey=uUEMKCROfsseS+8IzqPjzV3y1tzy4AkykwTib2jNkOFdzezF9s9XknqnIaf3CDft).

Para usar esse recurso, certifique-se de que o `Docker` esteja instalado na máquina. É necessário um ambiente sandbox dedicado do Docker para executar o código e impedir que códigos maliciosos gerados pelo LLM causem danos à máquina.

## Executar o AstrBot com Docker no Linux

Se você implantou o AstrBot usando Docker, será necessária uma configuração adicional.

1. Ao iniciar o contêiner Docker, monte `/var/run/docker.sock` dentro do contêiner. Isso permite que o AstrBot inicie contêineres sandbox.

```bash
sudo docker run -itd -p 6180-6200:6180-6200 -p 11451:11451 -v $PWD/data:/AstrBot/data -v /var/run/docker.sock:/var/run/docker.sock --name astrbot soulter/astrbot:latest
```

2. Durante a conversa, use o comando `/pi absdir <absolute-path>` para definir o caminho absoluto do diretório de dados do AstrBot na máquina host.

Exemplo:

![Exemplo de configuração do diretório]( /en/use/images/code-interpreter/image-4.png )

## Executar o AstrBot a partir do código-fonte no Linux

**Se os comandos do Docker exigirem privilégios de sudo**, inicie o AstrBot com `sudo`; caso contrário, o interpretador de código não conseguirá executar o Docker por falta de permissões.

```bash
sudo -E python3 main.py
```

## Como usar

Este recurso utiliza a imagem `soulter/astrbot-code-interpreter-sandbox`. Você pode consultar as informações detalhadas da imagem no [Docker Hub](https://hub.docker.com/r/soulter/astrbot-code-interpreter-sandbox).

A imagem inclui bibliotecas Python de uso comum:

- Pillow
- requests
- numpy
- matplotlib
- scipy
- scikit-learn
- beautifulsoup4
- pandas
- opencv-python
- python-docx
- python-pptx
- pymupdf
- mplfonts

Entre as tarefas possíveis estão:

- Edição de imagens
- Extração de dados de páginas da Web (*web scraping*)
- Análise de dados e aprendizado de máquina simples
- Processamento de documentos, como leitura e gravação de arquivos Word, PPT e PDF
- Cálculos matemáticos, como geração de gráficos e resolução de equações

Como o Docker Hub não é acessível a partir da China continental, se você estiver nessa região, use `/pi mirror` para consultar ou definir a origem do espelho. Por exemplo, na data em que esta documentação foi escrita, você pode definir `cjie.eu.org` como origem usando `/pi mirror cjie.eu.org`.

Na primeira vez em que o interpretador de código for acionado, o AstrBot baixará a imagem automaticamente. Isso pode levar algum tempo; aguarde.

A imagem pode receber atualizações periódicas para oferecer mais recursos. Verifique se há atualizações regularmente. Para atualizar a imagem, use o comando `/pi repull` para baixá-la novamente.

> [!TIP]
> Se o recurso não iniciar corretamente na primeira tentativa, depois que a inicialização for concluída com sucesso, execute `/tool on python_interpreter` para habilitá-lo.
> Use `/tool ls` para consultar todas as ferramentas e seus respectivos estados de ativação.

![Interpretador de código em execução]( /en/use/images/code-interpreter/image-3.png )

## Entrada de imagens e arquivos

Além de reconhecer e processar imagens e tarefas com texto, o interpretador de código também pode reconhecer arquivos enviados por você e devolver arquivos.

A partir da versão v3.4.34, use o comando `/pi file` para iniciar o envio de arquivos. Depois do envio, use `/pi list` para visualizar os arquivos enviados e `/pi clean` para limpá-los.

Os arquivos enviados serão utilizados como entrada do interpretador de código.

Por exemplo, se quiser arredondar os cantos de uma imagem, envie-a usando `/pi file` e depois peça: `Please run code to add rounded corners to this image`.

## Demonstração

![Demonstração do interpretador de código]( /en/use/images/code-interpreter/a3cd3a0e-aca5-41b2-aa52-66b568bd955b.png )

![Demonstração do interpretador de código]( /en/use/images/code-interpreter/image.png )

![Demonstração do interpretador de código]( /en/use/images/code-interpreter/image-1.png )

![Demonstração do interpretador de código]( /en/use/images/code-interpreter/image-2.png )
