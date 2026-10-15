"""Shared plugin error message templates for star manager flows."""

PLUGIN_ERROR_TEMPLATES = {
    "not_found_in_failed_list": "O plugin não está na lista de falhas.",
    "reserved_plugin_cannot_uninstall": "Este é um plugin reservado do AstrBot e não pode ser desinstalado.",
    "failed_plugin_dir_remove_error": (
        "O plugin com falha foi removido, mas não foi possível excluir sua pasta: {error}. Você pode removê-la manualmente em addons/plugins/."
    ),
}


def format_plugin_error(key: str, **kwargs) -> str:
    template = PLUGIN_ERROR_TEMPLATES.get(key, key)
    try:
        return template.format(**kwargs)
    except Exception:
        return template
