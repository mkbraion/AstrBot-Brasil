# Métodos de implantação disponibilizados pela comunidade

> [!WARNING]
> A equipe oficial do AstrBot não garante a segurança nem a estabilidade dos métodos de implantação apresentados nesta página.

## Script de instalação em um clique para Linux

Use `curl` para baixar o script e executá-lo com `bash`:

```bash
bash <(curl -sSL https://raw.githubusercontent.com/zhende1113/Antlia/refs/heads/main/Script/AstrBot/Antlia.sh)
```

Se o sistema não tiver o `curl` instalado, use `wget`:

```bash
wget -qO- https://raw.githubusercontent.com/zhende1113/Antlia/refs/heads/main/Script/AstrBot/Antlia.sh | bash
```

Repositório: [zhende1113/Antlia](https://github.com/zhende1113/Antlia/)

## Script de instalação em um clique para Linux (com Docker)

Compatível com AstrBot e NapCat.

> [!TIP]
> Se sua conta não tiver permissões suficientes, use `sudo` para executar o comando com privilégios elevados.

### Usando `curl`

```bash
curl -sSL https://raw.githubusercontent.com/railgun19457/AstrbotScript/main/AstrbotScript.sh -o AstrbotScript.sh
chmod +x AstrbotScript.sh
sudo ./AstrbotScript.sh
```

### Usando `wget`

```bash
wget -qO AstrbotScript.sh https://raw.githubusercontent.com/railgun19457/AstrbotScript/main/AstrbotScript.sh
chmod +x AstrbotScript.sh
sudo ./AstrbotScript.sh
```

> [!NOTE]
> Você também pode executar `sudo ./AstrbotScript.sh --no-color` para desativar a saída colorida.

Repositório: [railgun19457/AstrbotScript](https://github.com/railgun19457/AstrbotScript)

## Implantar o AstrBot no Android

Consulte o projeto [zz6zz666/AstrBot-Android-App](https://github.com/zz6zz666/AstrBot-Android-App).
