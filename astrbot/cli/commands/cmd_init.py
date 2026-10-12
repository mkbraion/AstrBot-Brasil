import asyncio
import os
from pathlib import Path

import click
from filelock import FileLock, Timeout

DASHBOARD_INITIAL_PASSWORD_ENV = "ASTRBOT_DASHBOARD_INITIAL_PASSWORD"


def _initialize_config_from_env(astrbot_root: Path) -> None:
    if DASHBOARD_INITIAL_PASSWORD_ENV not in os.environ:
        return

    from astrbot.core.config.astrbot_config import AstrBotConfig

    AstrBotConfig(config_path=str(astrbot_root / "data" / "cmd_config.json"))
    click.echo(
        "Configuração data/cmd_config.json inicializada com a senha inicial do dashboard."
    )


async def initialize_astrbot(astrbot_root: Path, yes: bool = False) -> None:
    """Executa a inicialização do AstrBot."""
    dot_astrbot = astrbot_root / ".astrbot"

    if not dot_astrbot.exists():
        if yes or click.confirm(
            f"Instalar o AstrBot Brasil neste diretório? {astrbot_root}",
            default=True,
            abort=True,
        ):
            dot_astrbot.touch()
            click.echo(f"Criado: {dot_astrbot}")

    paths = {
        "data": astrbot_root / "data",
        "config": astrbot_root / "data" / "config",
        "plugins": astrbot_root / "data" / "plugins",
        "temp": astrbot_root / "data" / "temp",
    }

    for _, path in paths.items():
        existed = path.exists()
        path.mkdir(parents=True, exist_ok=True)
        click.echo(f"{'Diretório existente' if existed else 'Criado'}: {path}")

    _initialize_config_from_env(astrbot_root)


@click.command()
@click.option("--yes", "-y", is_flag=True, help="Pula as perguntas de confirmação")
def init(yes: bool) -> None:
    """Inicializa o AstrBot Brasil."""
    from ..utils import get_astrbot_root

    click.echo("Inicializando o AstrBot Brasil...")

    astrbot_root = get_astrbot_root()
    lock_file = astrbot_root / "astrbot.lock"
    lock = FileLock(lock_file, timeout=5)

    try:
        with lock.acquire():
            asyncio.run(initialize_astrbot(astrbot_root, yes=yes))
            click.echo("Pronto! Execute 'astrbot run' para iniciar o AstrBot Brasil.")
    except Timeout:
        raise click.ClickException(
            "Não foi possível obter o arquivo de bloqueio. Verifique se outra instância está em execução."
        )
    except Exception as e:
        raise click.ClickException(f"Falha na inicialização: {e!s}")
