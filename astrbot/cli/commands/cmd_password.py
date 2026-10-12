import click

from .cmd_conf import (
    _load_config,
    _save_config,
    _set_dashboard_password,
    _set_nested_item,
    _validate_dashboard_password,
    _validate_dashboard_username,
)


@click.command(name="password")
@click.option(
    "--username",
    help="Usuário opcional do dashboard para alterar junto com a nova senha.",
)
def password(username: str | None) -> None:
    """Altera a senha do dashboard do AstrBot Brasil."""
    config = _load_config()

    new_password = click.prompt(
        "Nova senha do dashboard",
        hide_input=True,
        confirmation_prompt="Repita a nova senha para confirmar",
    )
    validated_password = _validate_dashboard_password(new_password)

    if username is not None:
        validated_username = _validate_dashboard_username(username.strip())
        _set_nested_item(config, "dashboard.username", validated_username)

    _set_dashboard_password(config, validated_password)
    _save_config(config)

    click.echo("Senha do dashboard atualizada.")
    if username is not None:
        click.echo(f"Usuário do dashboard atualizado: {validated_username}")
