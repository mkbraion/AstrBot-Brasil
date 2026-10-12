import re
import shutil
from pathlib import Path

import click

from ..utils import (
    PluginStatus,
    build_plug_list,
    check_astrbot_root,
    download_repository,
    get_astrbot_root,
    install_local_plugin,
    manage_plugin,
)


@click.group()
def plug() -> None:
    """Gerencia plugins do AstrBot Brasil."""


def _get_data_path() -> Path:
    base = get_astrbot_root()
    if not check_astrbot_root(base):
        raise click.ClickException(
            f"{base} não é um diretório raiz válido do AstrBot. Use 'astrbot init' para inicializar.",
        )
    return (base / "data").resolve()


def display_plugins(plugins, title=None, color=None) -> None:
    if title:
        click.echo(click.style(title, fg=color, bold=True))

    click.echo(
        f"{'Nome':<20} {'Versão':<10} {'Status':<10} {'Autor':<15} {'Descrição':<30}"
    )
    click.echo("-" * 85)

    for p in plugins:
        desc = p["desc"][:30] + ("..." if len(p["desc"]) > 30 else "")
        click.echo(
            f"{p['name']:<20} {p['version']:<10} {p['status']:<10} "
            f"{p['author']:<15} {desc:<30}",
        )


@plug.command()
@click.argument("name")
def new(name: str) -> None:
    """Cria um novo plugin."""
    base_path = _get_data_path()
    plug_path = base_path / "plugins" / name

    if plug_path.exists():
        raise click.ClickException(f"O plugin {name} já existe.")

    author = click.prompt("Autor do plugin", type=str)
    desc = click.prompt("Descrição do plugin", type=str)
    version = click.prompt("Versão do plugin", type=str)
    if not re.match(r"^\d+\.\d+(\.\d+)?$", version.lower().lstrip("v")):
        raise click.ClickException("A versão deve usar o formato x.y ou x.y.z.")
    repo = click.prompt("URL do repositório do plugin", type=str)
    if not repo.startswith("http"):
        raise click.ClickException("A URL do repositório deve começar com http ou https.")

    click.echo("Baixando o template do plugin...")
    download_repository(
        "https://github.com/Soulter/helloworld",
        plug_path,
    )

    click.echo("Atualizando os metadados do plugin...")
    with open(plug_path / "metadata.yaml", "w", encoding="utf-8") as f:
        f.write(
            f"name: {name}\n"
            f"desc: {desc}\n"
            f"version: {version}\n"
            f"author: {author}\n"
            f"repo: {repo}\n",
        )

    with open(plug_path / "README.md", "w", encoding="utf-8") as f:
        f.write(
            f"# {name}\n\n{desc}\n\n# Suporte\n\n[Documentação](https://docs.astrbot.app)\n"
        )

    with open(plug_path / "main.py", encoding="utf-8") as f:
        content = f.read()

    new_content = content.replace(
        '@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")',
        f'@register("{name}", "{author}", "{desc}", "{version}")',
    )

    with open(plug_path / "main.py", "w", encoding="utf-8") as f:
        f.write(new_content)

    click.echo(f"Plugin {name} criado com sucesso.")


@plug.command()
@click.option("--all", "-a", is_flag=True, help="Também lista plugins não instalados")
def list(all: bool) -> None:
    """Lista plugins."""
    base_path = _get_data_path()
    plugins = build_plug_list(base_path / "plugins")

    not_published_plugins = [
        p for p in plugins if p["status"] == PluginStatus.NOT_PUBLISHED
    ]
    if not_published_plugins:
        display_plugins(not_published_plugins, "Plugins não publicados", "red")

    need_update_plugins = [
        p for p in plugins if p["status"] == PluginStatus.NEED_UPDATE
    ]
    if need_update_plugins:
        display_plugins(need_update_plugins, "Plugins com atualização disponível", "yellow")

    installed_plugins = [p for p in plugins if p["status"] == PluginStatus.INSTALLED]
    if installed_plugins:
        display_plugins(installed_plugins, "Plugins instalados", "green")

    not_installed_plugins = [
        p for p in plugins if p["status"] == PluginStatus.NOT_INSTALLED
    ]
    if not_installed_plugins and all:
        display_plugins(not_installed_plugins, "Plugins não instalados", "blue")

    if (
        not any([not_published_plugins, need_update_plugins, installed_plugins])
        and not all
    ):
        click.echo("Nenhum plugin instalado.")


@plug.command()
@click.argument("name", required=False)
@click.option(
    "--editable",
    "-e",
    "local_path",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Instala um plugin de uma pasta local usando link simbólico",
)
@click.option("--proxy", help="Endereço do servidor proxy")
def install(name: str | None, local_path: Path | None, proxy: str | None) -> None:
    """Instala um plugin."""
    base_path = _get_data_path()
    plug_path = base_path / "plugins"

    if local_path is not None:
        install_local_plugin(local_path, plug_path, editable=True)
        return

    if name is None:
        raise click.ClickException("Informe o nome do plugin ou o caminho de um plugin local.")

    local_name_path = Path(name).expanduser()
    if local_name_path.exists() and local_name_path.is_dir():
        install_local_plugin(local_name_path, plug_path, editable=False)
        return

    plugins = build_plug_list(base_path / "plugins")

    plugin = next(
        (
            p
            for p in plugins
            if p["name"] == name and p["status"] == PluginStatus.NOT_INSTALLED
        ),
        None,
    )

    if not plugin:
        raise click.ClickException(f"Plugin {name} não encontrado ou já instalado.")

    manage_plugin(plugin, plug_path, is_update=False, proxy=proxy)


@plug.command()
@click.argument("name")
def remove(name: str) -> None:
    """Desinstala um plugin."""
    base_path = _get_data_path()
    plugins = build_plug_list(base_path / "plugins")
    plugin = next((p for p in plugins if p["name"] == name), None)

    if not plugin or not plugin.get("local_path"):
        raise click.ClickException(f"O plugin {name} não existe ou não está instalado.")

    plugin_path = plugin["local_path"]

    click.confirm(
        f"Tem certeza de que deseja desinstalar o plugin {name}?", default=False, abort=True
    )

    try:
        shutil.rmtree(plugin_path)
        click.echo(f"Plugin {name} desinstalado.")
    except Exception as e:
        raise click.ClickException(f"Falha ao desinstalar o plugin {name}: {e}")


@plug.command()
@click.argument("name", required=False)
@click.option("--proxy", help="Endereço de proxy do GitHub")
def update(name: str, proxy: str | None) -> None:
    """Atualiza plugins."""
    base_path = _get_data_path()
    plug_path = base_path / "plugins"
    plugins = build_plug_list(base_path / "plugins")

    if name:
        plugin = next(
            (
                p
                for p in plugins
                if p["name"] == name and p["status"] == PluginStatus.NEED_UPDATE
            ),
            None,
        )

        if not plugin:
            raise click.ClickException(
                f"O plugin {name} não precisa de atualização ou não pode ser atualizado."
            )

        manage_plugin(plugin, plug_path, is_update=True, proxy=proxy)
    else:
        need_update_plugins = [
            p for p in plugins if p["status"] == PluginStatus.NEED_UPDATE
        ]

        if not need_update_plugins:
            click.echo("Nenhum plugin precisa de atualização.")
            return

        click.echo(f"{len(need_update_plugins)} plugin(s) com atualização disponível.")
        for plugin in need_update_plugins:
            plugin_name = plugin["name"]
            click.echo(f"Atualizando plugin {plugin_name}...")
            manage_plugin(plugin, plug_path, is_update=True, proxy=proxy)


@plug.command()
@click.argument("query")
def search(query: str) -> None:
    """Pesquisa plugins."""
    base_path = _get_data_path()
    plugins = build_plug_list(base_path / "plugins")

    matched_plugins = [
        p
        for p in plugins
        if query.lower() in p["name"].lower()
        or query.lower() in p["desc"].lower()
        or query.lower() in p["author"].lower()
    ]

    if not matched_plugins:
        click.echo(f"Nenhum plugin correspondente a '{query}' foi encontrado.")
        return

    display_plugins(matched_plugins, f"Resultados da pesquisa: '{query}'", "cyan")
