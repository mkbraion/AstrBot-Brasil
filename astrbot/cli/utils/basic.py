from pathlib import Path

import click

# Arquivos estáticos incluídos no wheel instalado (gerados por hatch_build.py).
_BUNDLED_DIST = Path(__file__).parent.parent.parent / "dashboard" / "dist"


def check_astrbot_root(path: str | Path) -> bool:
    """Verifica se o caminho é um diretório raiz do AstrBot."""
    if not isinstance(path, Path):
        path = Path(path)
    if not path.exists() or not path.is_dir():
        return False
    if not (path / ".astrbot").exists():
        return False
    return True


def get_astrbot_root() -> Path:
    """Retorna o caminho do diretório raiz do AstrBot."""
    return Path.cwd()


async def check_dashboard(astrbot_root: Path) -> None:
    """Verifica se o dashboard está disponível."""
    from astrbot.core.updater import AstrBotUpdater

    # Quando o wheel já inclui o dashboard, não é necessário baixar novamente.
    if _BUNDLED_DIST.exists():
        click.echo("O dashboard já está incluído no pacote; download ignorado.")
        return

    try:
        dashboard_path = await AstrBotUpdater().ensure_dashboard()
        click.echo(f"Dashboard pronto em {dashboard_path}")
    except Exception as exc:
        click.echo(f"Falha ao preparar o Dashboard: {exc}")
