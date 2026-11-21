---
outline: deep
---

# Desenvolver um adaptador de plataforma

O AstrBot permite integrar adaptadores de plataforma na forma de plugins, possibilitando conectar plataformas que não são compatíveis nativamente, como Lark, DingTalk, mensagens privadas do Bilibili ou até mesmo Minecraft.

Usaremos uma plataforma chamada `FakePlatform` como exemplo.

Primeiro, adicione os arquivos `fake_platform_adapter.py` e `fake_platform_event.py` ao diretório do seu plugin. O primeiro implementa o adaptador da plataforma; o segundo define o evento da plataforma.

## Adaptador de plataforma

Suponha que o SDK cliente da FakePlatform tenha a seguinte estrutura:

```py
import asyncio


class FakeClient:
    """Simulates a messaging platform that sends a message every 5 seconds"""

    def __init__(self, token: str, username: str):
        self.token = token
        self.username = username
        # ...

    async def start_polling(self):
        while True:
            await asyncio.sleep(5)
            await getattr(self, "on_message_received")(
                {
                    "bot_id": "123",
                    "content": "new message",
                    "username": "zhangsan",
                    "userid": "123",
                    "message_id": "asdhoashd",
                    "group_id": "group123",
                }
            )

    async def send_text(self, to: str, message: str):
        print("Message sent:", to, message)

    async def send_image(self, to: str, image_path: str):
        print("Image sent:", to, image_path)
```

Agora, crie o arquivo `fake_platform_adapter.py`:

```py
import asyncio

from astrbot.api.platform import (
    Platform,
    AstrBotMessage,
    MessageMember,
    PlatformMetadata,
    MessageType,
)
from astrbot.api.event import MessageChain
from astrbot.api.message_components import (
    Plain,
    Image,
    Record,
)  # Componentes da cadeia de mensagens; importe conforme necessário
from astrbot.core.platform.message_session import MessageSesion
from astrbot.api.platform import register_platform_adapter
from astrbot import logger
from .client import FakeClient
from .fake_platform_event import FakePlatformEvent


# Registra o adaptador de plataforma. Parâmetros: nome, descrição e configuração padrão.
@register_platform_adapter(
    "fake",
    "fake adapter",
    default_config_tmpl={"token": "your_token", "username": "bot_username"},
)
class FakePlatformAdapter(Platform):
    def __init__(
        self, platform_config: dict, platform_settings: dict, event_queue: asyncio.Queue
    ) -> None:
        super().__init__(event_queue)
        self.config = platform_config  # Configuração padrão acima, preenchida pelo usuário e recebida aqui
        self.settings = platform_settings  # Configurações da plataforma

    async def send_by_session(
        self, session: MessageSesion, message_chain: MessageChain
    ):
        # Deve ser implementado
        await super().send_by_session(session, message_chain)

    def meta(self) -> PlatformMetadata:
        # Deve ser implementado. Basta retornar os metadados como no exemplo abaixo.
        return PlatformMetadata(
            "fake",
            "fake adapter",
        )

    async def run(self):
        # Deve ser implementado. Esta é a lógica principal.

        # FakeClient foi definido por nós; esta é apenas a função de callback usada no exemplo.
        async def on_received(data):
            logger.info(data)
            abm = await self.convert_message(data=data)  # Converte para AstrBotMessage
            await self.handle_msg(abm)

        # Inicializa o FakeClient
        self.client = FakeClient(self.config["token"], self.config["username"])
        self.client.on_message_received = on_received
        await (
            self.client.start_polling()
        )  # Escuta mensagens continuamente; esta chamada bloqueia a execução.

    async def convert_message(self, data: dict) -> AstrBotMessage:
        # Converte a mensagem da plataforma para AstrBotMessage.
        # O grau de adaptação é definido aqui. Cada plataforma possui uma estrutura de mensagem
        # diferente; faça a conversão de acordo com a estrutura correspondente.
        abm = AstrBotMessage()
        abm.type = (
            MessageType.GROUP_MESSAGE
        )  # Também pode ser friend_message em conversas privadas. Analise conforme a plataforma. Importante!
        abm.group_id = data["group_id"]  # Pode ser omitido em conversas privadas
        abm.message_str = data["content"]  # Mensagem em texto simples. Importante!
        abm.sender = MessageMember(
            user_id=data["userid"], nickname=data["username"]
        )  # Remetente. Importante!
        abm.message = [
            Plain(text=data["content"])
        ]  # Cadeia de mensagens. Acrescente outros tipos conforme necessário. Importante!
        abm.raw_message = data  # Mensagem original.
        abm.self_id = data["bot_id"]
        abm.session_id = data["userid"]  # ID da sessão. Importante!
        abm.message_id = data["message_id"]  # ID da mensagem.

        return abm

    async def handle_msg(self, message: AstrBotMessage):
        # Processa a mensagem
        message_event = FakePlatformEvent(
            message_str=message.message_str,
            message_obj=message,
            platform_meta=self.meta(),
            session_id=message.session_id,
            client=self.client,
        )
        self.commit_event(
            message_event
        )  # Envia o evento para a fila de eventos. Não se esqueça desta etapa!
```

Arquivo `fake_platform_event.py`:

```py
from astrbot.api.event import AstrMessageEvent, MessageChain
from astrbot.api.platform import AstrBotMessage, PlatformMetadata
from astrbot.api.message_components import Plain, Image
from .client import FakeClient


class FakePlatformEvent(AstrMessageEvent):
    def __init__(
        self,
        message_str: str,
        message_obj: AstrBotMessage,
        platform_meta: PlatformMetadata,
        session_id: str,
        client: FakeClient,
    ):
        super().__init__(message_str, message_obj, platform_meta, session_id)
        self.client = client

    async def send(self, message: MessageChain):
        for i in message.chain:  # Percorre a cadeia de mensagens
            if isinstance(i, Plain):  # Se for uma mensagem de texto
                await self.client.send_text(to=self.get_sender_id(), message=i.text)
            elif isinstance(i, Image):  # Se for uma imagem
                # convert_to_file_path() resolve referências de mídia compatíveis por meio
                # dos utilitários compartilhados de mídia.
                img_path = await i.convert_to_file_path()
                await self.client.send_image(
                    to=self.get_sender_id(), image_path=img_path
                )

        await super().send(
            message
        )  # Deve ser chamado ao final para executar o método send da classe pai.
```

## Tratamento de mensagens com mídia

Os adaptadores de plataforma não precisam reimplementar a análise de mídia para cada plataforma. Converta a mensagem recebida em componentes de mensagem do AstrBot e coloque a referência da mídia no campo `file` ou `url` do componente. São aceitos os seguintes formatos de referência:

- Caminho local, por exemplo, `/tmp/a.jpg`
- URI `file:` padrão, por exemplo, `file:///tmp/a.jpg`
- URL HTTP(S), por exemplo, `https://example.com/a.jpg`
- `base64://`, por exemplo, `base64://iVBORw0KGgo...`
- Data URI, por exemplo, `data:image/png;base64,iVBORw0KGgo...`
- Base64 simples legado, por exemplo, `iVBORw0KGgo...`; é aceito por compatibilidade, mas não deve ser gerado intencionalmente em código novo.

Se você já tiver um arquivo local, prefira os métodos de fábrica dos componentes. Eles geram URIs `file:` padronizadas:

```py
from astrbot.api.message_components import Image, Record, Video

abm.message.append(Image.fromFileSystem("/tmp/image.png"))
abm.message.append(Record.fromFileSystem("/tmp/audio.wav"))
abm.message.append(Video.fromFileSystem("/tmp/video.mp4"))
```

Se a plataforma fornecer uma URL acessível, passe-a diretamente ao componente:

```py
abm.message.append(Image(file=image_url, url=image_url))
abm.message.append(Record(file=audio_url, url=audio_url))
abm.message.append(Video(file=video_url, url=video_url))
```

Antes que os plugins e os provedores de LLM recebam o evento, a etapa de pré-processamento do AstrBot tenta normalizar as mídias da cadeia de mensagens:

- `Image` é materializado por meio dos utilitários compartilhados de mídia e convertido para JPEG quando necessário.
- `Record` é materializado pelos mesmos utilitários e convertido para WAV quando necessário.
- `Image` e `Record` dentro de cadeias `Reply` são normalizados da mesma maneira.
- Arquivos temporários criados pelo núcleo são associados ao evento atual e removidos quando o processamento do evento termina.

Ao enviar mensagens, se o SDK da plataforma exigir um caminho de arquivo local, chame `convert_to_file_path()` no componente em vez de verificar manualmente condições como `path.startswith("file://")`:

```py
if isinstance(i, Image):
    image_path = await i.convert_to_file_path()
    await self.client.send_image(to=self.get_sender_id(), image_path=image_path)
elif isinstance(i, Record):
    audio_path = await i.convert_to_file_path()
    await self.client.send_audio(to=self.get_sender_id(), audio_path=audio_path)
elif isinstance(i, Video):
    video_path = await i.convert_to_file_path()
    await self.client.send_video(to=self.get_sender_id(), video_path=video_path)
```

Se o próprio adaptador baixar mídias da plataforma para o diretório temporário do AstrBot, registre o caminho no evento depois de criar o arquivo, para que ele seja removido ao final do processamento:

```py
message_event.track_temporary_local_file(temp_media_path)
```

Por fim, em `main.py`, basta importar o módulo `fake_platform_adapter` durante a inicialização. O decorador fará o registro automaticamente.

```py
from astrbot.api.star import Context, Star


class MyPlugin(Star):
    def __init__(self, context: Context):
        from .fake_platform_adapter import FakePlatformAdapter  # noqa
```

Depois de configurar tudo, inicie o AstrBot:

![Exemplo do adaptador em execução](https://files.astrbot.app/docs/source/images/plugin-platform-adapter/QQ_1738155926221.png)

O adaptador `fake` que criamos agora aparece nesta tela.

![Adaptador listado na interface](https://files.astrbot.app/docs/source/images/plugin-platform-adapter/QQ_1738155982211.png)

Após a inicialização, você poderá confirmar que ele está funcionando corretamente:

![Adaptador em funcionamento](https://files.astrbot.app/docs/source/images/plugin-platform-adapter/QQ_1738156166893.png)

Se tiver dúvidas, participe do grupo da comunidade e pergunte por lá.
