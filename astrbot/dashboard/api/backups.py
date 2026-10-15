from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, Query, Request, UploadFile
from fastapi.responses import FileResponse

from astrbot.core import logger
from astrbot.dashboard.async_utils import run_maybe_async
from astrbot.dashboard.responses import error, ok
from astrbot.dashboard.schemas import (
    BackupImportRequest,
    BackupRenameRequest,
    BackupUploadInitRequest,
    BackupUploadSessionRequest,
)
from astrbot.dashboard.services.backup_service import (
    BackupService,
    BackupServiceError,
)

from .auth import AuthContext, require_dashboard_user, require_scope
from .multipart import UploadFileAdapter

router = APIRouter(tags=["Backups"])
legacy_router = APIRouter(
    prefix="/api/backup",
    tags=["Dashboard Backups"],
    include_in_schema=False,
)


def get_service(request: Request) -> BackupService:
    return request.app.state.services.backups


async def require_system_scope(request: Request) -> AuthContext:
    return await require_scope(request, "system")


def _model_dict(payload) -> dict:
    return payload.model_dump(exclude_none=True)


def _ok_result(result):
    if isinstance(result, tuple):
        data, message = result
        return ok(data, message)
    return ok(result)


def _safe_backup_filename(filename: str | None) -> str:
    if not filename:
        raise BackupServiceError("Parâmetro filename ausente")
    if ".." in filename or "/" in filename or "\\" in filename:
        raise BackupServiceError(
            "O nome do arquivo contém caracteres de caminho inválidos"
        )
    return filename


async def _json_or_empty(request: Request) -> dict:
    try:
        data = await request.json()
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


async def _run(operation, *, prefix: str):
    try:
        result = await run_maybe_async(operation)
        return _ok_result(result)
    except BackupServiceError as exc:
        return error(str(exc))
    except Exception as exc:
        logger.error("%s: %s", prefix, exc, exc_info=True)
        return error(f"{prefix}: {exc!s}")


def _download_response(download) -> FileResponse:
    return FileResponse(
        download.path,
        filename=download.filename,
        media_type="application/zip",
    )


def _download_backup(
    *,
    filename: str | None,
    token: str | None,
    service: BackupService,
):
    try:
        filename = _safe_backup_filename(filename)
        return _download_response(
            service.prepare_download(
                filename=filename,
                token=token,
                jwt_secret=service.config.get("dashboard", {}).get("jwt_secret"),
            )
        )
    except BackupServiceError as exc:
        return error(str(exc))
    except Exception as exc:
        logger.error("下载备份失败: %s", exc, exc_info=True)
        return error(f"Falha ao baixar o backup: {exc!s}")


@router.get("/backups")
async def list_backups(
    page: int = Query(default=1),
    page_size: int = Query(default=20),
    _auth: AuthContext = Depends(require_system_scope),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.list_backups(page=page, page_size=page_size),
        prefix="Falha ao obter a lista de backups",
    )


@legacy_router.get("/list")
async def list_dashboard_backups(
    page: int = Query(default=1),
    page_size: int = Query(default=20),
    _username: str = Depends(require_dashboard_user),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.list_backups(page=page, page_size=page_size),
        prefix="Falha ao obter a lista de backups",
    )


@router.post("/backups")
async def create_backup(
    _auth: AuthContext = Depends(require_system_scope),
    service: BackupService = Depends(get_service),
):
    return await _run(service.export_backup, prefix="Falha ao criar o backup")


@legacy_router.post("/export")
async def export_dashboard_backup(
    _username: str = Depends(require_dashboard_user),
    service: BackupService = Depends(get_service),
):
    return await _run(service.export_backup, prefix="Falha ao criar o backup")


@router.post("/backups/upload")
async def upload_backup(
    file: UploadFile = File(...),
    _auth: AuthContext = Depends(require_system_scope),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.upload_backup(UploadFileAdapter(file)),
        prefix="Falha ao enviar o arquivo de backup",
    )


@legacy_router.post("/upload")
async def upload_dashboard_backup(
    file: UploadFile = File(...),
    _username: str = Depends(require_dashboard_user),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.upload_backup(UploadFileAdapter(file)),
        prefix="Falha ao enviar o arquivo de backup",
    )


@router.post("/backups/upload/init")
async def init_backup_upload(
    payload: BackupUploadInitRequest,
    auth: AuthContext = Depends(require_system_scope),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.upload_init(_model_dict(payload), owner=auth.username),
        prefix="Falha ao iniciar o envio em partes",
    )


@legacy_router.post("/upload/init")
async def init_dashboard_backup_upload(
    payload: BackupUploadInitRequest,
    username: str = Depends(require_dashboard_user),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.upload_init(_model_dict(payload), owner=username),
        prefix="Falha ao iniciar o envio em partes",
    )


@router.post("/backups/upload/chunk")
async def upload_backup_chunk(
    upload_id: str = Form(...),
    chunk_index: str = Form(...),
    chunk: UploadFile = File(...),
    auth: AuthContext = Depends(require_system_scope),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.upload_chunk(
            upload_id=upload_id,
            chunk_index_str=chunk_index,
            chunk_file=UploadFileAdapter(chunk),
            owner=auth.username,
        ),
        prefix="Falha ao enviar a parte",
    )


@legacy_router.post("/upload/chunk")
async def upload_dashboard_backup_chunk(
    upload_id: str = Form(...),
    chunk_index: str = Form(...),
    chunk: UploadFile = File(...),
    username: str = Depends(require_dashboard_user),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.upload_chunk(
            upload_id=upload_id,
            chunk_index_str=chunk_index,
            chunk_file=UploadFileAdapter(chunk),
            owner=username,
        ),
        prefix="Falha ao enviar a parte",
    )


@router.post("/backups/upload/complete")
async def complete_backup_upload(
    payload: BackupUploadSessionRequest,
    auth: AuthContext = Depends(require_system_scope),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.upload_complete(_model_dict(payload), owner=auth.username),
        prefix="Falha ao concluir o envio em partes",
    )


@legacy_router.post("/upload/complete")
async def complete_dashboard_backup_upload(
    payload: BackupUploadSessionRequest,
    username: str = Depends(require_dashboard_user),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.upload_complete(_model_dict(payload), owner=username),
        prefix="Falha ao concluir o envio em partes",
    )


@router.post("/backups/upload/abort")
async def abort_backup_upload(
    payload: BackupUploadSessionRequest,
    auth: AuthContext = Depends(require_system_scope),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.upload_abort(_model_dict(payload), owner=auth.username),
        prefix="Falha ao cancelar o envio",
    )


@legacy_router.post("/upload/abort")
async def abort_dashboard_backup_upload(
    payload: BackupUploadSessionRequest,
    username: str = Depends(require_dashboard_user),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.upload_abort(_model_dict(payload), owner=username),
        prefix="Falha ao cancelar o envio",
    )


@router.post("/backups/upload/status")
async def status_backup_upload(
    payload: BackupUploadSessionRequest,
    auth: AuthContext = Depends(require_system_scope),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.upload_status(_model_dict(payload), owner=auth.username),
        prefix="Falha ao consultar o estado do envio",
    )


@legacy_router.post("/upload/status")
async def status_dashboard_backup_upload(
    payload: BackupUploadSessionRequest,
    username: str = Depends(require_dashboard_user),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.upload_status(_model_dict(payload), owner=username),
        prefix="Falha ao consultar o estado do envio",
    )


@router.get("/backups/tasks/{task_id}")
async def get_backup_progress(
    task_id: str,
    _auth: AuthContext = Depends(require_system_scope),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.get_progress(task_id),
        prefix="Falha ao obter o progresso da tarefa",
    )


@legacy_router.get("/progress")
async def get_dashboard_backup_progress(
    task_id: str | None = Query(default=None),
    _username: str = Depends(require_dashboard_user),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.get_progress(task_id),
        prefix="Falha ao obter o progresso da tarefa",
    )


@router.get("/backups/{filename:path}")
async def download_backup(
    filename: str,
    request: Request,
    token: str | None = Query(default=None),
    service: BackupService = Depends(get_service),
):
    if not token:
        auth_header = request.headers.get("Authorization", "").strip()
        scheme, separator, credentials = auth_header.partition(" ")
        if separator and scheme.lower() == "bearer":
            token = credentials.strip() or None
    return _download_backup(filename=filename, token=token, service=service)


@legacy_router.get("/download")
async def download_dashboard_backup(
    filename: str | None = Query(default=None),
    token: str | None = Query(default=None),
    service: BackupService = Depends(get_service),
):
    return _download_backup(filename=filename, token=token, service=service)


@router.patch("/backups/{filename:path}")
async def rename_backup(
    filename: str,
    payload: BackupRenameRequest,
    _auth: AuthContext = Depends(require_system_scope),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.rename_backup(
            {"filename": _safe_backup_filename(filename), **_model_dict(payload)}
        ),
        prefix="Falha ao renomear o backup",
    )


@legacy_router.post("/rename")
async def rename_dashboard_backup(
    payload: BackupRenameRequest,
    filename: str | None = Query(default=None),
    _username: str = Depends(require_dashboard_user),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.rename_backup({"filename": filename, **_model_dict(payload)}),
        prefix="Falha ao renomear o backup",
    )


@router.delete("/backups/{filename:path}")
async def delete_backup(
    filename: str,
    _auth: AuthContext = Depends(require_system_scope),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.delete_backup({"filename": _safe_backup_filename(filename)}),
        prefix="Falha ao excluir o backup",
    )


@legacy_router.post("/delete")
async def delete_dashboard_backup(
    request: Request,
    filename: str | None = Query(default=None),
    _username: str = Depends(require_dashboard_user),
    service: BackupService = Depends(get_service),
):
    body = await _json_or_empty(request)
    return await _run(
        lambda: service.delete_backup({"filename": filename, **body}),
        prefix="Falha ao excluir o backup",
    )


@router.post("/backups/{filename:path}/check")
async def check_backup(
    filename: str,
    _auth: AuthContext = Depends(require_system_scope),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.check_backup({"filename": _safe_backup_filename(filename)}),
        prefix="Falha na verificação prévia do backup",
    )


@legacy_router.post("/check")
async def check_dashboard_backup(
    request: Request,
    filename: str | None = Query(default=None),
    _username: str = Depends(require_dashboard_user),
    service: BackupService = Depends(get_service),
):
    body = await _json_or_empty(request)
    return await _run(
        lambda: service.check_backup({"filename": filename, **body}),
        prefix="Falha na verificação prévia do backup",
    )


@router.post("/backups/{filename:path}/import")
async def import_backup(
    filename: str,
    payload: BackupImportRequest,
    _auth: AuthContext = Depends(require_system_scope),
    service: BackupService = Depends(get_service),
):
    return await _run(
        lambda: service.import_backup(
            {"filename": _safe_backup_filename(filename), **_model_dict(payload)}
        ),
        prefix="Falha ao importar o backup",
    )


@legacy_router.post("/import")
async def import_dashboard_backup(
    request: Request,
    filename: str | None = Query(default=None),
    _username: str = Depends(require_dashboard_user),
    service: BackupService = Depends(get_service),
):
    body = await _json_or_empty(request)
    return await _run(
        lambda: service.import_backup({"filename": filename, **body}),
        prefix="Falha ao importar o backup",
    )
