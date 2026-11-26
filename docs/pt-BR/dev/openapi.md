---
outline: deep
---

# API HTTP do AstrBot

A partir da versão v4.18.0, o AstrBot disponibiliza APIs HTTP baseadas em chaves de API para acesso programático.

## Início rápido

1. Na WebUI, acesse `Configurações → OpenAPI` e clique em `Criar chave de API`.
2. Inclua a chave de API nos cabeçalhos da requisição:

```http
Authorization: Bearer abk_xxx
```

Também é aceito:

```http
X-API-Key: abk_xxx
```

3. Para os endpoints de chat, o campo `username` é obrigatório:

- `POST /api/v1/chat`: o corpo da requisição deve incluir `username`
- `GET /api/v1/chat/sessions`: os parâmetros de consulta devem incluir `username`

O esquema OpenAPI local está disponível em `http://localhost:6185/api/v1/openapi.json`, e a documentação interativa está disponível em `http://localhost:6185/api/v1/docs`.

## Permissões de escopo

As chaves de API podem ser configuradas com `scopes`. Consulte a [Referência de escopos de API e endpoints](./openapi-scopes.md) para conhecer a finalidade de cada escopo, as regras de herança e a lista completa de endpoints.

Se a chave de API não incluir o escopo exigido pelo endpoint de destino, a requisição retornará `403 Insufficient API key scope`.

- `config` não vem selecionado por padrão na WebUI e inclui automaticamente `bot` e `provider`.
- `config:edit_admin` e `chat:admin` precisam ser concedidos explicitamente e nunca são herdados de seus escopos principais.
- Ao desmarcar `bot` ou `provider` na WebUI, o escopo dependente `config` também é removido.

Atualmente, as chaves de API para desenvolvedores oferecem suporte a 11 escopos de nível superior e dois subescopos sensíveis. `tool`, `skills`, `kb` e `system` não são escopos válidos para chaves de API de desenvolvedor. Use o escopo singular `skill` para os endpoints `/api/v1/skills/*`.

Cada operação na referência interativa também exibe `Required scope: ...`; operações que envolvem recursos administrativos exibem adicionalmente `Conditional sensitive scope: ...`.

## Endpoints comuns

**Chat**

Interaja com o Agent integrado do AstrBot. Há suporte a chamadas de plugins, chamadas de ferramentas e outros recursos — de forma consistente com o chat pelo mensageiro instantâneo (IM).

- `POST /api/v1/chat`: envia uma mensagem de chat (fluxo SSE; o servidor gera um UUID quando `session_id` é omitido)
- `GET /api/v1/chat/sessions`: lista sessões de um `username` específico, com paginação
- `GET /api/v1/configs`: lista os arquivos de configuração disponíveis
- `POST /api/v1/file`: envia um anexo para uso posterior em segmentos de mensagem

**Bots e provedores**

- `GET /api/v1/bots`: lista as configurações de bots e plataformas
- `POST /api/v1/bots`: cria uma configuração de bot ou plataforma
- `GET /api/v1/providers`: lista as configurações de provedores de modelos
- `GET /api/v1/provider-sources`: lista as configurações das fontes de provedores

**Personas, plugins, MCP e Skills**

- `GET /api/v1/personas`: lista as personas
- `GET /api/v1/plugins`: lista os plugins
- `GET /api/v1/mcp/servers`: lista os servidores MCP
- `GET /api/v1/skills`: lista as Skills

**Mensagens IM proativas**

- `POST /api/v1/im/message`: envia uma mensagem proativa por meio de UMO
- `GET /api/v1/im/bots`: lista os IDs de bots e plataformas

## Formato do campo `message` (importante)

O campo `message` em `POST /api/v1/chat` e `POST /api/v1/im/message` aceita dois formatos:

1. String: mensagem de texto simples
2. Array: segmentos de mensagem (cadeia de mensagens)

### 1. Formato de texto simples

```json
{
  "message": "Olá"
}
```

### 2. Formato de array de segmentos de mensagem

```json
{
  "message": [
    { "type": "plain", "text": "Consulte este arquivo, por favor" },
    { "type": "file", "attachment_id": "9a2f8c72-e7af-4c0e-b352-111111111111" }
  ]
}
```

Valores de `type` aceitos:

| type | Campos obrigatórios | Campos opcionais | Descrição |
| --- | --- | --- | --- |
| `plain` | `text` | - | Segmento de texto |
| `reply` | `message_id` | `selected_text` | Resposta citando uma mensagem |
| `image` | `attachment_id` | - | Segmento de anexo de imagem |
| `record` | `attachment_id` | - | Segmento de anexo de áudio |
| `file` | `attachment_id` | - | Segmento de arquivo genérico |
| `video` | `attachment_id` | - | Segmento de anexo de vídeo |

* Atualmente, o segmento `reply` é aceito apenas em `/api/v1/chat`, não em `POST /api/v1/im/message`.

Observações:

- `attachment_id` vem de um registro de anexo existente ou de `POST /api/v1/file`, após o envio de um anexo com o escopo `file`.
- `reply` não pode ser o único segmento; é necessário pelo menos um segmento com conteúdo (por exemplo, `plain/image/file/...`).
- Uma requisição contendo apenas `reply` ou conteúdo vazio retornará um erro.

### Uso de `message` na API de Chat

`POST /api/v1/chat` também exige `username` e aceita `session_id` opcional (um UUID é gerado automaticamente quando o campo é omitido).

`username` é uma identidade do WebChat declarada pelo chamador e usada como remetente da mensagem e proprietária da sessão. Uma chave que tenha apenas `chat` será rejeitada quando o valor corresponder a qualquer ID de administrador configurado e não poderá receber uma função administrativa dentro do pipeline de mensagens. O subescopo sensível `chat:admin` permite explicitamente o uso de IDs de administradores configurados; ele não transforma nomes de usuário arbitrários em administradores. Ainda assim, as integrações devem associar usuários externos a nomes de usuário estáveis e controlados pela aplicação.

```json
{
  "username": "alice",
  "session_id": "my_session_001",
  "message": [
    { "type": "plain", "text": "Resuma este PDF, por favor" },
    { "type": "file", "attachment_id": "9a2f8c72-e7af-4c0e-b352-111111111111" }
  ],
  "enable_streaming": true
}
```

### Uso de `message` na API de mensagens IM

`POST /api/v1/im/message` exige `umo` + `message`.

```json
{
  "umo": "webchat:FriendMessage:openapi_probe",
  "message": [
    { "type": "plain", "text": "Esta é uma mensagem proativa" },
    { "type": "image", "attachment_id": "9a2f8c72-e7af-4c0e-b352-222222222222" }
  ]
}
```

## Exemplo

```bash
curl -N 'http://localhost:6185/api/v1/chat' \
  -H 'Authorization: Bearer abk_xxx' \
  -H 'Content-Type: application/json' \
  -d '{"message":"Olá","username":"alice"}'
```

## Referência completa da API

Consulte a documentação interativa:

- https://docs.astrbot.app/scalar.html
