import json
import zoneinfo
from collections.abc import Callable
from typing import Any

import click

from ..utils import check_astrbot_root, get_astrbot_root


def _validate_log_level(value: str) -> str:
    """Valida o nível de log."""
    value = value.upper()
    if value not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise click.ClickException(
            "O nível de log deve ser DEBUG, INFO, WARNING, ERROR ou CRITICAL.",
        )
    return value


def _validate_dashboard_port(value: str) -> int:
    """Valida a porta do Dashboard."""
    try:
        port = int(value)
        if port < 1 or port > 65535:
            raise click.ClickException("A porta deve estar entre 1 e 65535.")
        return port
    except ValueError:
        raise click.ClickException("A porta deve ser um número.")


def _validate_dashboard_username(value: str) -> str:
    """Valida o usuário do Dashboard."""
    if not value:
        raise click.ClickException("O usuário não pode ficar vazio.")
    return value


def _validate_dashboard_password(value: str) -> str:
    """Valida a senha do Dashboard."""
    from astrbot.core.utils.auth_password import validate_dashboard_password

    try:
        validate_dashboard_password(value)
    except ValueError as e:
        raise click.ClickException(str(e))
    return value


def _validate_timezone(value: str) -> str:
    """Valida o fuso horário."""
    try:
        zoneinfo.ZoneInfo(value)
    except Exception:
        raise click.ClickException(
            f"Fuso horário inválido: {value}. Use um nome IANA válido, como America/Sao_Paulo."
        )
    return value


def _validate_callback_api_base(value: str) -> str:
    """Valida a URL base da API de callback."""
    if not value.startswith("http://") and not value.startswith("https://"):
        raise click.ClickException(
            "A URL base da API de callback deve começar com http:// ou https://."
        )
    return value


# Chaves técnicas configuráveis pela CLI. Os nomes permanecem inalterados
# para preservar compatibilidade com a configuração do AstrBot.
CONFIG_VALIDATORS: dict[str, Callable[[str], Any]] = {
    "timezone": _validate_timezone,
    "log_level": _validate_log_level,
    "dashboard.port": _validate_dashboard_port,
    "dashboard.username": _validate_dashboard_username,
    "dashboard.password": _validate_dashboard_password,
    "callback_api_base": _validate_callback_api_base,
}


def _load_config() -> dict[str, Any]:
    """Carrega ou inicializa o arquivo de configuração."""
    root = get_astrbot_root()
    if not check_astrbot_root(root):
        raise click.ClickException(
            f"{root} não é um diretório raiz válido do AstrBot. Use 'astrbot init' para inicializar.",
        )

    config_path = root / "data" / "cmd_config.json"
    if not config_path.exists():
        from astrbot.core.config.default import DEFAULT_CONFIG

        config_path.write_text(
            json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2),
            encoding="utf-8-sig",
        )

    try:
        return json.loads(config_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as e:
        raise click.ClickException(f"Falha ao interpretar o arquivo de configuração: {e!s}")


def _save_config(config: dict[str, Any]) -> None:
    """Salva o arquivo de configuração."""
    config_path = get_astrbot_root() / "data" / "cmd_config.json"

    config_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding="utf-8-sig",
    )


def _set_nested_item(obj: dict[str, Any], path: str, value: Any) -> None:
    """Define um valor em um dicionário aninhado."""
    parts = path.split(".")
    for part in parts[:-1]:
        if part not in obj:
            obj[part] = {}
        elif not isinstance(obj[part], dict):
            raise click.ClickException(
                f"Conflito no caminho da configuração: {'.'.join(parts[: parts.index(part) + 1])} não é um objeto.",
            )
        obj = obj[part]
    obj[parts[-1]] = value


def _get_nested_item(obj: dict[str, Any], path: str) -> Any:
    """Obtém um valor de um dicionário aninhado."""
    parts = path.split(".")
    for part in parts:
        obj = obj[part]
    return obj


def _set_dashboard_password(config: dict[str, Any], raw_password: str) -> None:
    """Define os hashes da senha e limpa indicadores de migração."""
    from astrbot.core.utils.auth_password import (
        hash_dashboard_password,
        hash_md5_dashboard_password,
    )

    _set_nested_item(
        config,
        "dashboard.pbkdf2_password",
        hash_dashboard_password(raw_password),
    )
    _set_nested_item(
        config,
        "dashboard.password",
        hash_md5_dashboard_password(raw_password),
    )
    _set_nested_item(config, "dashboard.password_storage_upgraded", True)
    _set_nested_item(config, "dashboard.password_change_required", False)


@click.group(name="conf")
def conf() -> None:
    """Gerencia configurações pela CLI.

    Chaves suportadas:

    - timezone: fuso horário (ex.: America/Sao_Paulo)
    - log_level: nível de log (DEBUG/INFO/WARNING/ERROR/CRITICAL)
    - dashboard.port: porta do dashboard
    - dashboard.username: usuário do dashboard
    - dashboard.password: senha do dashboard
    - callback_api_base: URL base da API de callback
    """


@conf.command(name="set")
@click.argument("key")
@click.argument("value")
def set_config(key: str, value: str) -> None:
    """Define o valor de uma configuração."""
    if key not in CONFIG_VALIDATORS:
        raise click.ClickException(f"Chave de configuração não suportada: {key}")

    config = _load_config()

    try:
        old_value = _get_nested_item(config, key)
        validated_value = CONFIG_VALIDATORS[key](value)
        if key == "dashboard.password":
            _set_dashboard_password(config, validated_value)
        else:
            _set_nested_item(config, key, validated_value)
        _save_config(config)

        click.echo(f"Configuração atualizada: {key}")
        if key == "dashboard.password":
            click.echo("  Valor anterior: ********")
            click.echo("  Novo valor: ********")
        else:
            click.echo(f"  Valor anterior: {old_value}")
            click.echo(f"  Novo valor: {validated_value}")

    except KeyError:
        raise click.ClickException(f"Chave de configuração desconhecida: {key}")
    except Exception as e:
        raise click.UsageError(f"Falha ao definir a configuração: {e!s}")


@conf.command(name="get")
@click.argument("key", required=False)
def get_config(key: str | None = None) -> None:
    """Exibe uma configuração ou todas as configurações disponíveis."""
    config = _load_config()

    if key:
        if key not in CONFIG_VALIDATORS:
            raise click.ClickException(f"Chave de configuração não suportada: {key}")

        try:
            value = _get_nested_item(config, key)
            if key == "dashboard.password":
                value = "********"
            click.echo(f"{key}: {value}")
        except KeyError:
            raise click.ClickException(f"Chave de configuração desconhecida: {key}")
        except Exception as e:
            raise click.UsageError(f"Falha ao obter a configuração: {e!s}")
    else:
        click.echo("Configuração atual:")
        for key in CONFIG_VALIDATORS:
            try:
                value = (
                    "********"
                    if key == "dashboard.password"
                    else _get_nested_item(config, key)
                )
                click.echo(f"  {key}: {value}")
            except (KeyError, TypeError):
                pass
