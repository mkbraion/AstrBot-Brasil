# Imagens de entrada dos modelos

O construtor do agente principal (`build_main_agent`) prepara as imagens de entrada iniciais antes da geração de legendas ou da inicialização do agente. Isso abrange anexos comuns, imagens citadas, imagens de `ProviderRequest` de plugins e chamadas diretas ao construtor. Depois de `OnLLMRequestEvent`, o fluxo processa apenas referências de imagem recém-introduzidas; as referências existentes reutilizam os resultados já preparados, sem uma nova verificação dos arquivos.

## Limites e formatos

- Arquivos de imagem originais maiores que **64 MiB** são ignorados antes que seu conteúdo seja lido ou que seus pixels sejam decodificados. O motivo da omissão e o caminho original preservado são salvos no histórico. Uma notificação temporária sugere usar a ferramenta de leitura de arquivos, se disponível, ou pedir ao usuário que envie uma imagem menor; essa orientação não é salva. Arquivos de até 64 MiB, inclusive, são processados normalmente.
- Cada arquivo de imagem preparado tem tamanho **estritamente inferior a 512 KiB** (524.288 bytes). Esse limite se aplica aos bytes da imagem antes da codificação em Base64, não ao tamanho total da solicitação.
- O **comprimento máximo da borda das imagens de entrada**, em **Configuração**, continua configurável por meio de `provider_settings.image_compress_options.max_size` (padrão de 1280 pixels). As imagens iniciais mantêm a proporção e nunca são ampliadas. Elas podem ser reduzidas ainda mais para atender ao limite de bytes. As imagens introduzidas pelo gancho da solicitação seguem o mesmo limite configurado para as bordas, as regras de formato e animação, o limite de entrada de 64 MiB e o limite estrito de saída de 512 KiB.
- Imagens JPEG/PNG com orientação correta que já estejam dentro dos dois limites preservam seus bytes originais. Outras imagens estáticas têm a orientação corrigida e são codificadas como JPEG ou, quando possuem transparência, como PNG. As imagens transparentes preservam o canal alfa mesmo quando é necessário reduzi-las ainda mais.
- Imagens GIF, WebP animadas e APNG são convertidas em uma montagem branca de quadros em grade 3×3. São incluídos até nove quadros espaçados uniformemente, incluindo o primeiro e o último quadros da animação; as células não utilizadas ficam em branco. Um quadro de capa independente de APNG é excluído.
- Metadados desnecessários são removidos durante a recodificação. O perfil de cores é preservado quando é compatível com o formato de saída e com o limite de bytes.

Esses limites também se aplicam aos anexos do usuário em sessões CUA. Capturas de tela e outras imagens resultantes de ferramentas seguem seu próprio tratamento.

## Alterações na configuração

| Configuração anterior | Comportamento atual |
| --- | --- |
| Ativar compactação de imagens (`image_compress_enabled`) | Removida; as imagens de entrada atuais são sempre preparadas. |
| Qualidade JPEG (`image_compress_options.quality`) | Removida; o tamanho da saída é controlado automaticamente. |
| Comprimento máximo da borda (`image_compress_options.max_size`) | Renomeado para **Comprimento máximo da borda das imagens de entrada**; é aplicado em conjunto com o limite estrito de 512 KiB. |

Os valores das configurações removidas em arquivos de configuração existentes não afetam mais a preparação das imagens.

## Arquivos originais e ciclo de vida das pré-visualizações

A etapa de preparação de imagens adiciona avisos de texto comuns, como `Image N`, com os caminhos originais e as origens das mensagens citadas. A numeração segue a ordem dos blocos de imagem após os ganchos e a filtragem, incluindo partes de conteúdo de imagem anteriores a `image_urls`. Nenhum metadado de anexo é adicionado aos modelos de solicitação ou de mensagem. As origens citadas e os resultados de legendas gerados com sucesso são encaminhados diretamente pelas respectivas etapas de processamento; o texto dos avisos nunca é analisado para inferir o estado. Somente os objetos de aviso gerados pela solicitação atual são atualizados depois dos ganchos, preservando o texto fornecido pelos plugins. Imagens ignoradas mantêm um motivo sem numeração e o caminho original; os rótulos de animação identificam a montagem 3×3. Imagens processadas por um modelo de geração de legendas são identificadas no texto, sem ocupar um índice visual na solicitação principal.

`image_urls` e as partes de conteúdo de imagem reutilizam diretamente arquivos JPEG/PNG locais que já estejam em conformidade; nenhuma cópia de trabalho é criada. Imagens que precisam de conversão usam arquivos de pré-visualização preparados. Os caminhos dos anexos apresentados ao modelo para acesso a arquivos continuam apontando para as **imagens originais**, permitindo que as ferramentas leiam os originais. Os arquivos originais e os componentes de imagem do evento não são sobrescritos.

Os arquivos de pré-visualização pertencem ao evento atual e são excluídos quando o evento termina, inclusive em caso de falha ou cancelamento. Não existe um cache compartilhado de conversão de imagens. Referências repetidas dentro da mesma solicitação reutilizam a mesma pré-visualização, inclusive na etapa de preparação posterior ao gancho da solicitação.

Anexos originais associados com sucesso ao evento, incluindo imagens citadas, sobrevivem à limpeza do evento. Os originais preservados no diretório temporário continuam sujeitos à limpeza por `temp_dir_max_size` e não constituem armazenamento permanente. As fontes que ainda não tiverem sido incorporadas com sucesso quando a coleta da solicitação falhar continuam sob responsabilidade do evento.

O histórico da conversa captura o conteúdo de imagem preparado como Data URIs em Base64 antes que os arquivos de pré-visualização expirem. O histórico antigo não é processado novamente. Uma imagem ilegível é ignorada; textos válidos e outras imagens são mantidos. Cancelamentos, esgotamento de recursos e erros de programação não são tratados como imagens inválidas.

Backends de Agent de terceiros, chamadas diretas a provedores que ignoram o construtor do agente principal e imagens resultantes de ferramentas estão fora deste fluxo de preparação de imagens de entrada.
