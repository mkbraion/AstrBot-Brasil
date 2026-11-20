# Conectar implementações do protocolo OneBot v11

> [!TIP]
> Se você pretende conectar o AstrBot ao QQ, recomendamos usar o [Bot Oficial do QQ (WebSockets)](/en/platform/qqofficial/websockets). Essa integração é fornecida oficialmente pelo QQ, oferece maior estabilidade e permite fazer login com um clique usando a leitura de um QR Code.

O OneBot é uma interface padronizada para aplicações de bots, criada para unificar o desenvolvimento de bots em diferentes plataformas de conversa. Assim, os desenvolvedores podem implementar a lógica de negócio uma única vez e utilizá-la em várias plataformas.

O AstrBot oferece suporte a todas as implementações cliente compatíveis com OneBot v11 por meio de Reverse WebSocket, com o AstrBot atuando como servidor.

Alguns projetos que implementam o OneBot v11:

- [NapCat](https://github.com/NapNeko/NapCatQQ)
- [OneDisc](https://github.com/ITCraftDevelopmentTeam/OneDisc)
- [Tele-KiraLink](https://github.com/Echomirix/Tele-KiraLink)

Consulte a documentação de implantação de cada projeto.

## 1. Configurar o OneBot v11

1. Abra a WebUI do AstrBot.
2. Clique em `Platforms` na barra lateral esquerda.
3. Clique em `Add Adapter`, acima da lista de bots.
4. Selecione `OneBot v11`.

Preencha o formulário:

- **ID (`id`):** informe qualquer valor. Ele serve apenas para diferenciar instâncias de plataformas distintas.
- **Ativar (`enable`):** marque esta opção.
- **Host do Reverse WebSocket:** informe o IP da sua máquina; normalmente, use `0.0.0.0`.
- **Porta do Reverse WebSocket:** escolha uma porta. O padrão é `6199`.
- **Token do Reverse WebSocket:** preencha este campo somente se houver um token configurado na rede do NapCat.

Clique em `Save`.

## 2. Configurar o lado da implementação do protocolo

Consulte a documentação de implantação do projeto que implementa o protocolo.

Observações:

1. A implementação precisa oferecer suporte a `Reverse WebSocket`. Nesse modelo, o AstrBot atua como servidor e o cliente da implementação atua como cliente.
2. A URL do Reverse WebSocket é `ws(s)://<your-host>:6199/ws`.

## 3. Verificar a conexão

Na WebUI do AstrBot, acesse `Data & Logs` -> `Logs`. Se aparecer um registro azul com a mensagem `aiocqhttp(OneBot v11) adapter connected.`, a conexão foi estabelecida.

Se, após alguns segundos, aparecer `aiocqhttp adapter has been closed`, a conexão expirou e falhou. Confira novamente as configurações.
