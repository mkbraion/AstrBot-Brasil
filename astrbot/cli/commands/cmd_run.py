import asyncio
import os
import sys
import traceback
from pathlib import Path

import click
from filelock import FileLock, Timeout

from ..utils import check_astrbot_root, check_dashboard, get_astrbot_root

DASHBOARD_RESET_PASSWORD_ENV = "ASTRBOT_RESET_DASHBOARD_PASSWORD"


async def run_astrbot(astrbot_root: Path) -> None:
    """Executa o AstrBot Brasil."""
    from astrbot.core import LogBroker, LogManager, db_helper, logger
    from astrbot.core.initial_loader import InitialLoader

    await check_dashboard(astrbot_root / "data")

    log_broker = LogBroker()
    LogManager.set_queue_handler(logger, log_broker)
    db = db_helper

    core_lifecycle = InitialLoader(db, log_broker)

    await core_lifecycle.start()


@click.option(
    "--reload",
    "-r",
    is_flag=True,
    help="Recarrega plugins automaticamente durante o desenvolvimento",
)
@click.option(
    "--port", "-p", help="Porta do Dashboard do AstrBot", required=False, type=str
)
@click.option(
    "--reset-password",
    is_flag=True,
    help="Redefine a senha inicial do dashboard ao iniciar",
)
@click.command()
def run(reload: bool, port: str | None, reset_password: bool) -> None:
    """Inicia o AstrBot Brasil."""
    try:
        os.environ["ASTRBOT_CLI"] = "1"
        astrbot_root = get_astrbot_root()

        if not check_astrbot_root(astrbot_root):
            raise click.ClickException(
                f"{astrbot_root} não é um diretório raiz válido do AstrBot. Use 'astrbot init' para inicializar.",
            )

        os.environ["ASTRBOT_ROOT"] = str(astrbot_root)
        sys.path.insert(0, str(astrbot_root))

        if port:
            os.environ["DASHBOARD_PORT"] = port

        if reload:
            click.echo("Recarga automática de plugins ativada.")
            os.environ["ASTRBOT_RELOAD"] = "1"

        if reset_password:
            os.environ[DASHBOARD_RESET_PASSWORD_ENV] = "1"

        lock_file = astrbot_root / "astrbot.lock"
        lock = FileLock(lock_file, timeout=5)
        with lock.acquire():
            asyncio.run(run_astrbot(astrbot_root))
    except KeyboardInterrupt:
        click.echo("AstrBot Brasil encerrado.")
    except Timeout:
        raise click.ClickException(
            "Não foi possível obter o arquivo de bloqueio. Verifique se outra instância está em execução."
        )
    except Exception as e:
        raise click.ClickException(
            f"Erro durante a execução: {e}\n{traceback.format_exc()}"
        )
