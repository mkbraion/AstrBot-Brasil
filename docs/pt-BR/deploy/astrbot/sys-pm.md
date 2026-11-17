# Instalação por gerenciador de pacotes do sistema

> [!WARNING]
> Atualmente, somente a versão para AUR está disponível.
> Se você usa Windows ou macOS, recomenda-se instalar pelo `uv`.
> Se você usa Linux, recomenda-se fortemente instalar por meio de um gerenciador de pacotes.

# Preparação

## O que é AUR?

O AUR (Arch User Repository) permite instalar softwares de repositórios mantidos pela comunidade. Os pacotes do AUR geralmente são mantidos por membros da comunidade, e não pelos mantenedores oficiais do projeto.

Entre os auxiliares de AUR mais conhecidos estão `yay` e `paru`.

O tutorial a seguir usa o `paru` como exemplo. O `yay` funciona de maneira semelhante; basta substituir `paru` por `yay` nos comandos.

# Processo de instalação

## AUR

```bash
paru -S astrbot-git
# Observação:
# A etapa de revisão será iniciada; pressione 'q' para sair da revisão e continuar a instalação.
# Após a instalação, o diretório de dados será fixado em: ~/.local/share/astrbot
```

# Iniciar

> [!TIP]
> Na primeira execução, você pode usar diretamente `astrbot init` para inicializar o sistema.
> Em seguida, use `astrbot run` para iniciar o bot.
> Ainda assim, recomenda-se usar o `systemctl`, pois ele oferece recursos como reinicialização automática e rotação de logs.

```bash
systemctl --user start astrbot.service
```

# Iniciar automaticamente com o sistema

```bash
# Por segurança, o serviço foi configurado para ser executado como usuário.
systemctl --user enable astrbot.service
# Para habilitar e iniciar imediatamente, adicione --now.
# systemctl --user enable --now astrbot.service
```
