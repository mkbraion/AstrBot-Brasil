# Instalação pelo gerenciador de pacotes (uv)

Use o `uv` para instalar e executar o AstrBot rapidamente.

## Antes de começar

Se o `uv` ainda não estiver instalado, siga o guia oficial para instalá-lo:

<https://docs.astral.sh/uv/>

O `uv` é compatível com Linux, Windows e macOS.

## Observações importantes

> [!WARNING]
> Uma instalação do AstrBot feita com `uv` **não oferece suporte à atualização pela WebUI**. Para atualizar, execute `uv tool upgrade astrbot --python 3.12` no terminal.

O AstrBot requer Python 3.12 ou superior. Use `--python 3.12` para garantir que o `uv` crie o ambiente da ferramenta com Python 3.12. Se o download de versões do Python estiver habilitado, o `uv` baixará automaticamente o Python 3.12 caso ele ainda não esteja instalado.

## Instalar e iniciar

```bash
uv tool install astrbot --python 3.12
astrbot
```
