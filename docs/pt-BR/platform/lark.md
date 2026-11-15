# Conectar ao Lark

## Tipos de mensagem compatíveis

> Versão v4.16.0.

| Tipo de mensagem | Receber | Enviar | Observações |
| --- | --- | --- | --- |
| Texto | Sim | Sim | |
| Imagem | Sim | Sim | |
| Áudio | Sim | Sim | Convertido para WAV ao receber e para Opus ao enviar |
| Vídeo | Sim | Sim | Convertido para MP4 antes do envio |
| Arquivo | Sim | Sim | |

Ao receber uma mensagem citada (resposta), o AstrBot interpreta o texto, as imagens, os vídeos e os arquivos citados.

Em conversas em grupo, o bot responde às mensagens que mencionam o bot com `@mention`, mencionam todos os participantes (a menos que essa opção esteja desativada), respondem a uma mensagem dele ou começam com um prefixo de ativação, como `/`.

**Envio proativo de mensagens:** compatível.

**Saída em streaming:** compatível. No Console de Desenvolvedores do Lark, habilite para o aplicativo a permissão `Create and update cards (cardkit:card:write)`.

A versão do cliente Lark deve ser igual ou superior a 7.20. Versões anteriores exibem apenas o título e uma solicitação para atualizar o aplicativo.

## Criar um bot

O Lark oferece dois métodos de configuração: criação por QR Code diretamente no AstrBot ou criação manual de um aplicativo empresarial personalizado no Console de Desenvolvedores do Lark.

### Opção 1: criação por QR Code

Requisito: AstrBot na versão v4.25.0 ou superior.

Abra o painel de gerenciamento do AstrBot, clique em `Platforms` na barra lateral esquerda, clique em `Add Adapter` e selecione `lark`.

Em `Creation Method`, selecione `One-click QR Creation`, escolha a edição da China ou a edição internacional, conforme necessário, leia o QR Code com o aplicativo móvel Lark e confirme. Quando a criação for concluída, o AstrBot preencherá automaticamente `app_id`, `app_secret` e a configuração de domínio do aplicativo.

> [!IMPORTANT]
> Por padrão, em conversas em grupo, o Lark envia ao AstrBot somente as mensagens que mencionam o bot com `@mention`. Para que o bot receba todas as mensagens do grupo, habilite a permissão `im:message.group_msg` no Console de Desenvolvedores do Lark.
>
> Substitua `<APP_ID>` na URL abaixo pelo ID do seu aplicativo Lark e abra o endereço para acessar diretamente a página de habilitação de permissões.
>
> Para localizar o App ID, volte à página `Platforms` do AstrBot, selecione o bot Lark que acabou de criar e consulte `app_id` em `Connection settings`.
>
> ```text
> https://open.feishu.cn/app/<APP_ID>/auth?q=contact:contact.base:readonly,contact:user.base:readonly,im:message,im:message.p2p_msg:readonly,im:message.group_at_msg:readonly,im:message.group_msg,im:message:send_as_bot,im:resource,cardkit:card:write&op_from=openapi&token_type=tenant
> ```

Depois que a criação por QR Code for concluída, continue com as etapas de assinatura de eventos, permissões, publicação da versão e inclusão do bot em grupos descritas abaixo.

### Opção 2: criação manual

Acesse o [Console de Desenvolvedores](https://open.feishu.cn/app) e crie um aplicativo empresarial personalizado.

![Criar aplicativo empresarial personalizado](https://files.astrbot.app/docs/source/images/lark/image.png)

Adicione a capacidade de bot ao aplicativo.

![Adicionar capacidade de bot](https://files.astrbot.app/docs/source/images/lark/image-1.png)

Clique em `Credentials & Basic Info` para obter `app_id` e `app_secret`.

![Obter app_id e app_secret](https://files.astrbot.app/docs/source/images/lark/image-4.png)

## Configurar o AstrBot

1. Acesse o painel de gerenciamento do AstrBot.
2. Clique em `Platforms` na barra lateral esquerda.
3. Clique em `Add Adapter`, acima da lista de bots.
4. Selecione `lark`.
5. Se quiser que o AstrBot crie o aplicativo, selecione `One-click QR Creation` e conclua a leitura do QR Code. Se você já criou o aplicativo, selecione `Manual Creation`.

Preencha os campos de configuração:

- `ID`: escolha um identificador para distinguir diferentes instâncias da plataforma de mensagens.
- `Enable`: marque esta opção.
- `app_id`: informe o `app_id` obtido anteriormente.
- `app_secret`: informe o `app_secret` obtido anteriormente.

No campo de domínio, mantenha o valor padrão se estiver usando o Lark da China. Para a edição internacional, informe `https://open.larksuite.com`. Se estiver usando uma instância empresarial do Lark hospedada por você, informe o domínio dessa instância.

Quanto ao método de assinatura, `socket` usa uma conexão persistente, enquanto `webhook` envia eventos ao servidor do desenvolvedor e exige um servidor publicamente acessível. Em geral, recomendamos `socket`; tanto o Lark da China quanto o internacional oferecem suporte a conexões persistentes. Em uma instância do Lark hospedada por você, escolha `webhook` se as conexões persistentes não estiverem disponíveis. As etapas seguintes variam conforme a opção escolhida.

Se você selecionou `webhook`, acesse o Console de Desenvolvedores do Lark, clique em `Events & Callbacks` e depois em `Encryption Policy`. Preencha o campo `Encrypt Key`. Embora não seja obrigatório, recomendamos fortemente configurar essa proteção para aumentar a segurança dos dados. Depois, copie `Encrypt Key` e `Verification Token` para os campos correspondentes do AstrBot: `Encrypt Key` (`lark_encrypt_key`) e `Verification Token` (`lark_verification_token`).

Clique em `Save`.

## Configurar callbacks e permissões

As etapas a seguir dependem do método de assinatura selecionado. Siga a seção correspondente à sua configuração.

### Método de conexão persistente `socket`

Clique em `Events & Callbacks`, selecione `Receive events using long connection` e clique em `Save`.

**Se a conexão iniciada na etapa anterior não tiver sido estabelecida com sucesso, não será possível salvar esta configuração.**

![Configurar Events & Callbacks](https://files.astrbot.app/docs/source/images/lark/image-6.png)

### Método `webhook`: enviar eventos ao servidor do desenvolvedor

> [!TIP]
> Para configurar esse método corretamente, consulte também o [modo de Webhook unificado](/pt-BR/use/unified-webhook), que apresenta as configurações necessárias.

Depois de clicar em `Save`, selecione o bot em `Platforms` e clique em `View Webhook URL` para copiar a URL de callback.

Volte à página `Events & Callbacks` do Lark, clique em `Event Configuration`, selecione `Send events to developer server`, informe a URL copiada no campo `Request URL` e clique em `Save`. Se tudo estiver configurado corretamente, nenhum erro será exibido.

### Configurar eventos

Depois de concluir a configuração de eventos da etapa anterior, clique em `Add Event`, acesse `Messages & Groups`, role a página até localizar `Receive Message` e adicione esse evento.

![Adicionar evento](https://files.astrbot.app/docs/source/images/lark/image-7.png)

Habilite as permissões indicadas a seguir.

![Habilitar permissões](https://files.astrbot.app/docs/source/images/lark/image-8.png)

Em seguida, clique em `Save`, na parte superior da página.

Acesse `Permission Management`, clique em `Enable Permissions` e informe `im:message,im:message:send_as_bot`. Adicione as permissões filtradas.

Informe `im:resource` para habilitar o envio e o recebimento de imagens, arquivos e outros recursos.

Habilite `contact:contact.base:readonly` e `contact:user.base:readonly` para que os remetentes de mensagens privadas sejam identificados pelo nome de exibição.

Para usar o bot em conversas em grupo, habilite também `im:message.group_at_msg:readonly` e `im:message.group_msg`.

> [!TIP]
> Um aplicativo criado pelo método de QR Code recebe, por padrão, somente as mensagens de grupo que mencionam o bot com `@mention`. Para receber todas as mensagens do grupo, confirme que `im:message.group_msg` está habilitada. Você também pode usar a URL de permissões apresentada anteriormente para abrir rapidamente a página correspondente.

Para usar a saída em streaming, habilite também `Create and update cards (cardkit:card:write)`.

O conjunto final de permissões deve ser semelhante ao da imagem:

![Permissões finais](https://files.astrbot.app/docs/source/images/lark/image-11.png)

## Criar uma versão

Crie uma nova versão do aplicativo.

![Criar versão](https://files.astrbot.app/docs/source/images/lark/image-2.png)

Preencha o número da versão, as notas da atualização e o escopo de visibilidade. Depois, clique em `Save` e confirme a publicação.

## Adicionar o bot a um grupo

Abra o aplicativo Lark. A versão Web não oferece suporte à inclusão de bots. Entre em uma conversa em grupo, clique no botão no canto superior direito, acesse `Group Bots` → `Add Bot`.

Pesquise o bot que acabou de criar. Por exemplo, se você criou o bot `AstrBot`, como neste tutorial:

![Adicionar bot](https://files.astrbot.app/docs/source/images/lark/image-9.png)

## 🎉 Concluído!

Mencione o bot no grupo e envie o comando `/help`. O bot deverá responder.

![Integração concluída](https://files.astrbot.app/docs/source/images/lark/image-13.png)
