"""Ponto de entrada da CLI do AstrBot Brasil."""

import sys

import click

from . import __version__
from .commands import conf, init, password, plug, run

logo_tmpl = r"""
     ___           _______.___________..______      .______     ______   .___________.
    /   \         /       |           ||   _  \     |   _  \   /  __  \  |           |
   /  ^  \       |   (----`---|  |----`|  |_)  |    |  |_)  | |  |  |  | `---|  |----`
  /  /_\  \       \   \       |  |     |      /     |   _  <  |  |  |  |     |  |
 /  _____  \  .----)   |      |  |     |  |\  \----.|  |_)  | |  `--'  |     |  |
/__/     \__\ |_______/       |__|     | _| `._____||______/   \______/      |__|
"""


@click.group()
@click.version_option(__version__, prog_name="AstrBot Brasil")
def cli() -> None:
    """CLI do AstrBot Brasil."""
    click.echo(logo_tmpl)
    click.echo("Bem-vindo à CLI do AstrBot Brasil! 🇧🇷")
    click.echo(f"Versão da CLI: {__version__}")


@click.command()
@click.argument("command_name", required=False, type=str)
def help(command_name: str | None) -> None:
    """Exibe ajuda dos comandos.

    Informe COMMAND_NAME para ver detalhes de um comando específico.
    Sem argumento, exibe a ajuda geral da CLI.
    """
    ctx = click.get_current_context()
    if command_name:
        command = cli.get_command(ctx, command_name)
        if command:
            click.echo(command.get_help(ctx))
        else:
            click.echo(f"Comando desconhecido: {command_name}")
            sys.exit(1)
    else:
        click.echo(cli.get_help(ctx))


cli.add_command(init)
cli.add_command(run)
cli.add_command(help)
cli.add_command(plug)
cli.add_command(conf)
cli.add_command(password)

if __name__ == "__main__":
    cli()
