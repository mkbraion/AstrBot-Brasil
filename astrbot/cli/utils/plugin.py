import shutil
import tempfile
import uuid
from enum import Enum
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import click
import httpx
import yaml

from .version_comparator import VersionComparator


class PluginStatus(str, Enum):
    INSTALLED = "installed"
    NEED_UPDATE = "needs-update"
    NOT_INSTALLED = "not-installed"
    NOT_PUBLISHED = "unpublished"


LOCAL_PLUGIN_COPY_IGNORE = shutil.ignore_patterns(
    ".git",
    "__pycache__",
    "*.pyc",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
    ".zed",
)


def _validate_plugin_dir_name(plugin_name: str, source_path: Path) -> str:
    plugin_name = plugin_name.strip()
    plugin_path = Path(plugin_name)
    has_separator = "/" in plugin_name or "\\" in plugin_name
    if (
        not plugin_name
        or plugin_name in {".", ".."}
        or plugin_path.is_absolute()
        or has_separator
        or plugin_path.name != plugin_name
    ):
        raise click.ClickException(
            f"O metadata.yaml do plugin local {source_path} possui um nome inválido: {plugin_name}"
        )
    return plugin_name


def download_repository(
    url: str,
    target_path: Path,
    proxy: str | None = None,
) -> None:
    """Baixa o código-fonte de um repositório sem exigir Git instalado localmente.

    Args:
        url: URL de repositório compatível.
        target_path: Pasta que receberá os arquivos do repositório.
        proxy: Prefixo de proxy opcional para a solicitação do arquivo compactado.
    """
    from astrbot.core.repository import GitHubRepository

    temp_dir = Path(tempfile.mkdtemp())
    try:
        repository = GitHubRepository.parse(url)
        reference = (
            f"branch {repository.branch}"
            if repository.branch
            else "referência padrão HEAD"
        )
        click.echo(
            f"Baixando {repository.owner}/{repository.name} do GitHub ({reference})..."
        )
        download_url = repository.archive_url
        if proxy:
            download_url = f"{proxy.rstrip('/')}/{download_url}"

        with httpx.Client(follow_redirects=True, trust_env=True) as client:
            response = client.get(download_url)
            response.raise_for_status()
            zip_content = BytesIO(response.content)
        with ZipFile(zip_content) as z:
            z.extractall(temp_dir)
            namelist = z.namelist()
            root_dir = Path(namelist[0]).parts[0] if namelist else ""
            if target_path.exists():
                shutil.rmtree(target_path)
            shutil.move(temp_dir / root_dir, target_path)
    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


def load_yaml_metadata(plugin_dir: Path) -> dict:
    """Carrega os metadados do plugin a partir de metadata.yaml."""
    yaml_path = plugin_dir / "metadata.yaml"
    if yaml_path.exists():
        try:
            return yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
        except Exception as e:
            click.echo(f"Falha ao ler {yaml_path}: {e}", err=True)
    return {}


def build_plug_list(plugins_dir: Path) -> list:
    """Monta a lista de plugins locais e disponíveis online."""
    result = []
    if plugins_dir.is_dir():
        for plugin_dir in plugins_dir.iterdir():
            if not plugin_dir.is_dir():
                continue

            metadata = load_yaml_metadata(plugin_dir)

            if "desc" not in metadata and "description" in metadata:
                metadata["desc"] = metadata["description"]

            if metadata and all(
                k in metadata for k in ["name", "desc", "version", "author", "repo"]
            ):
                result.append(
                    {
                        "name": str(metadata.get("name", "")),
                        "desc": str(metadata.get("desc", "")),
                        "version": str(metadata.get("version", "")),
                        "author": str(metadata.get("author", "")),
                        "repo": str(metadata.get("repo", "")),
                        "status": PluginStatus.INSTALLED,
                        "local_path": str(plugin_dir),
                    },
                )

    online_plugins_dict = {}
    try:
        with httpx.Client() as client:
            resp = client.get("https://api.soulter.top/astrbot/plugins")
            resp.raise_for_status()
            data = resp.json()
            for plugin_id, plugin_info in data.items():
                online_plugins_dict[str(plugin_id)] = {
                    "name": str(plugin_id),
                    "desc": str(plugin_info.get("desc", "")),
                    "version": str(plugin_info.get("version", "")),
                    "author": str(plugin_info.get("author", "")),
                    "repo": str(plugin_info.get("repo", "")),
                    "status": PluginStatus.NOT_INSTALLED,
                    "local_path": None,
                }
    except Exception as e:
        click.echo(f"Falha ao carregar a lista de plugins online: {e}", err=True)

    for local_plugin in result:
        online_plugin = online_plugins_dict.pop(local_plugin["name"], None)
        if online_plugin is None:
            local_plugin["status"] = PluginStatus.NOT_PUBLISHED
            continue

        if (
            VersionComparator.compare_version(
                local_plugin["version"],
                online_plugin["version"],
            )
            < 0
        ):
            local_plugin["status"] = PluginStatus.NEED_UPDATE

    result.extend(online_plugins_dict.values())
    return result


def _cleanup_local_plugin_target(target_path: Path) -> None:
    if target_path.is_symlink() or target_path.is_file():
        target_path.unlink(missing_ok=True)
    elif target_path.exists():
        shutil.rmtree(target_path, ignore_errors=True)


def _copy_local_plugin(source_path: Path, plugins_dir: Path, target_path: Path) -> None:
    temp_target = plugins_dir / f".{target_path.name}.tmp-{uuid.uuid4().hex}"
    try:
        shutil.copytree(source_path, temp_target, ignore=LOCAL_PLUGIN_COPY_IGNORE)
        temp_target.rename(target_path)
    except FileExistsError:
        raise click.ClickException(
            f"O plugin {target_path.name} já existe."
        ) from None
    except Exception:
        raise
    finally:
        if temp_target.exists() or temp_target.is_symlink():
            _cleanup_local_plugin_target(temp_target)


def install_local_plugin(
    source_path: Path,
    plugins_dir: Path,
    editable: bool = False,
) -> None:
    """Instala um plugin a partir de uma pasta local."""
    source_path = source_path.expanduser().resolve()
    plugins_dir = plugins_dir.resolve()

    if not source_path.exists() or not source_path.is_dir():
        raise click.ClickException(f"O caminho do plugin local não existe: {source_path}")

    metadata = load_yaml_metadata(source_path)
    plugin_name = metadata.get("name")
    if not isinstance(plugin_name, str) or not plugin_name.strip():
        raise click.ClickException(
            f"O plugin local {source_path} precisa conter metadata.yaml com um nome válido."
        )
    plugin_name = _validate_plugin_dir_name(plugin_name, source_path)

    target_path = plugins_dir / plugin_name
    if target_path.exists():
        raise click.ClickException(f"O plugin {plugin_name} já existe.")

    try:
        plugins_dir.mkdir(parents=True, exist_ok=True)
        if editable:
            try:
                target_path.symlink_to(source_path, target_is_directory=True)
            except OSError as e:
                raise click.ClickException(
                    f"Falha ao criar o link simbólico para a instalação editável: {e}. "
                    "No Windows, talvez seja necessário executar como Administrador ou ativar o Modo de Desenvolvedor."
                ) from e
        else:
            _copy_local_plugin(source_path, plugins_dir, target_path)
        click.echo(f"Plugin {plugin_name} instalado com sucesso a partir de {source_path}.")
    except FileExistsError:
        raise click.ClickException(f"O plugin {plugin_name} já existe.") from None
    except click.ClickException:
        raise
    except Exception as e:
        if editable and target_path.is_symlink():
            _cleanup_local_plugin_target(target_path)
        raise click.ClickException(
            f"Erro ao instalar o plugin local {plugin_name}: {e}"
        ) from e


def manage_plugin(
    plugin: dict,
    plugins_dir: Path,
    is_update: bool = False,
    proxy: str | None = None,
) -> None:
    """Instala ou atualiza um plugin."""
    plugin_name = plugin["name"]
    repo_url = plugin["repo"]

    if is_update and plugin.get("local_path"):
        target_path = Path(plugin["local_path"])
    else:
        target_path = plugins_dir / plugin_name

    backup_path = Path(f"{target_path}_backup") if is_update else None

    if is_update and not target_path.exists():
        raise click.ClickException(
            f"O plugin {plugin_name} não está instalado e não pode ser atualizado."
        )

    if is_update and backup_path is not None and backup_path.exists():
        shutil.rmtree(backup_path)
    if is_update and backup_path is not None:
        shutil.copytree(target_path, backup_path)

    try:
        action = "Atualizando" if is_update else "Baixando"
        click.echo(f"{action} plugin {plugin_name} de {repo_url}...")
        download_repository(repo_url, target_path, proxy)

        if is_update and backup_path is not None and backup_path.exists():
            shutil.rmtree(backup_path)
        completed = "atualizado" if is_update else "instalado"
        click.echo(f"Plugin {plugin_name} {completed} com sucesso.")
    except Exception as e:
        if target_path.exists():
            shutil.rmtree(target_path, ignore_errors=True)
        if is_update and backup_path is not None and backup_path.exists():
            shutil.move(backup_path, target_path)
        action = "atualizar" if is_update else "instalar"
        raise click.ClickException(
            f"Erro ao {action} o plugin {plugin_name}: {e}",
        )
