from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request

from astrbot.core import logger
from astrbot.dashboard.async_utils import run_maybe_async
from astrbot.dashboard.responses import error, ok
from astrbot.dashboard.schemas import (
    BatchSessionProviderRequest,
    BatchSessionServiceRequest,
    SessionGroupRequest,
    SessionRuleRequest,
    UmoListRequest,
)
from astrbot.dashboard.services.session_management_service import (
    SessionManagementService,
    SessionManagementServiceError,
)

from .auth import AuthContext, ScopeDependency, require_dashboard_user

router = APIRouter(tags=["Sessions"])
legacy_router = APIRouter(
    prefix="/api/session",
    tags=["Dashboard Sessions"],
    include_in_schema=False,
)


def get_service(request: Request) -> SessionManagementService:
    return request.app.state.services.sessions


require_data_scope = ScopeDependency("data")


async def _json_or_empty(request: Request) -> dict:
    try:
        data = await request.json()
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _service_error(exc: SessionManagementServiceError) -> dict:
    return error(str(exc))


def _unexpected_error(prefix: str, exc: Exception) -> dict:
    logger.error(f"{prefix}: {exc!s}")
    return error(f"{prefix}: {exc!s}")


async def _run(operation, *, label: str) -> dict:
    try:
        result = await run_maybe_async(operation)
        return ok(result)
    except SessionManagementServiceError as exc:
        return _service_error(exc)
    except Exception as exc:
        return _unexpected_error(label, exc)


async def _run_dashboard_json(
    request: Request,
    operation,
    *,
    label: str,
) -> dict:
    body = await _json_or_empty(request)
    return await _run(lambda: operation(body), label=label)


@router.get("/sessions")
async def list_sessions(
    page: int = Query(1),
    page_size: int = Query(20),
    search: str = Query(""),
    message_type: str = Query("all"),
    platform: str = Query(""),
    _auth: AuthContext = Depends(require_data_scope),
    service: SessionManagementService = Depends(get_service),
):
    try:
        return ok(
            await service.list_all_umos_with_status(
                page=page,
                page_size=page_size,
                search=search.strip(),
                message_type=message_type,
                platform=platform,
            )
        )
    except SessionManagementServiceError as exc:
        return _service_error(exc)
    except Exception as exc:
        return _unexpected_error("Falha ao obter os estados das sessões", exc)


@router.get("/sessions/active-umos")
async def list_active_umos(
    _auth: AuthContext = Depends(require_data_scope),
    service: SessionManagementService = Depends(get_service),
):
    try:
        return ok(await service.list_active_umos())
    except SessionManagementServiceError as exc:
        return _service_error(exc)
    except Exception as exc:
        return _unexpected_error("Falha ao obter a lista de UMO", exc)


@router.get("/sessions/rules")
async def list_session_rules(
    page: int = Query(1),
    page_size: int = Query(10),
    search: str = Query(""),
    _auth: AuthContext = Depends(require_data_scope),
    service: SessionManagementService = Depends(get_service),
):
    try:
        return ok(
            await service.list_session_rules(
                page=page,
                page_size=page_size,
                search=search.strip(),
            )
        )
    except SessionManagementServiceError as exc:
        return _service_error(exc)
    except Exception as exc:
        return _unexpected_error("Falha ao obter as regras", exc)


@router.post("/sessions/rules")
async def update_session_rule(
    payload: SessionRuleRequest,
    _auth: AuthContext = Depends(require_data_scope),
    service: SessionManagementService = Depends(get_service),
):
    try:
        return ok(
            await service.update_session_rule(payload.model_dump(exclude_none=True))
        )
    except SessionManagementServiceError as exc:
        return _service_error(exc)
    except Exception as exc:
        return _unexpected_error("Falha ao atualizar as regras da sessão", exc)


@router.post("/sessions/rules/delete")
async def delete_session_rule(
    payload: UmoListRequest,
    _auth: AuthContext = Depends(require_data_scope),
    service: SessionManagementService = Depends(get_service),
):
    try:
        return ok(
            await service.delete_session_rules(payload.model_dump(exclude_none=True))
        )
    except SessionManagementServiceError as exc:
        return _service_error(exc)
    except Exception as exc:
        return _unexpected_error("Falha ao excluir as regras da sessão", exc)


@router.patch("/sessions/provider")
async def update_session_provider(
    payload: BatchSessionProviderRequest,
    _auth: AuthContext = Depends(require_data_scope),
    service: SessionManagementService = Depends(get_service),
):
    try:
        return ok(
            await service.batch_update_provider(payload.model_dump(exclude_none=True))
        )
    except SessionManagementServiceError as exc:
        return _service_error(exc)
    except Exception as exc:
        return _unexpected_error("Falha ao atualizar provedores em lote", exc)


@router.patch("/sessions/service")
async def update_session_service(
    payload: BatchSessionServiceRequest,
    _auth: AuthContext = Depends(require_data_scope),
    service: SessionManagementService = Depends(get_service),
):
    try:
        return ok(
            await service.batch_update_service(payload.model_dump(exclude_none=True))
        )
    except SessionManagementServiceError as exc:
        return _service_error(exc)
    except Exception as exc:
        return _unexpected_error(
            "Falha ao atualizar os estados dos serviços em lote", exc
        )


@router.get("/session-groups")
async def list_session_groups(
    _auth: AuthContext = Depends(require_data_scope),
    service: SessionManagementService = Depends(get_service),
):
    try:
        return ok(await service.list_groups())
    except SessionManagementServiceError as exc:
        return _service_error(exc)
    except Exception as exc:
        return _unexpected_error("Falha ao obter os grupos", exc)


@router.post("/session-groups")
async def create_session_group(
    payload: SessionGroupRequest,
    _auth: AuthContext = Depends(require_data_scope),
    service: SessionManagementService = Depends(get_service),
):
    try:
        return ok(await service.create_group(payload.model_dump(exclude_none=True)))
    except SessionManagementServiceError as exc:
        return _service_error(exc)
    except Exception as exc:
        return _unexpected_error("Falha ao criar o grupo", exc)


@router.put("/session-groups/{group_id}")
async def update_session_group(
    group_id: str,
    payload: SessionGroupRequest,
    _auth: AuthContext = Depends(require_data_scope),
    service: SessionManagementService = Depends(get_service),
):
    try:
        body = payload.model_dump(exclude_none=True)
        return ok(await service.update_group({"group_id": group_id, **body}))
    except SessionManagementServiceError as exc:
        return _service_error(exc)
    except Exception as exc:
        return _unexpected_error("Falha ao atualizar o grupo", exc)


@router.delete("/session-groups/{group_id}")
async def delete_session_group(
    group_id: str,
    _auth: AuthContext = Depends(require_data_scope),
    service: SessionManagementService = Depends(get_service),
):
    try:
        return ok(await service.delete_group({"group_id": group_id}))
    except SessionManagementServiceError as exc:
        return _service_error(exc)
    except Exception as exc:
        return _unexpected_error("Falha ao excluir o grupo", exc)


@legacy_router.get("/list-rule")
async def list_dashboard_session_rules(
    page: int = Query(1),
    page_size: int = Query(10),
    search: str = Query(""),
    _username: str = Depends(require_dashboard_user),
    service: SessionManagementService = Depends(get_service),
):
    return await _run(
        lambda: service.list_session_rules(
            page=page,
            page_size=page_size,
            search=search.strip(),
        ),
        label="Falha ao obter as regras",
    )


@legacy_router.post("/update-rule")
async def update_dashboard_session_rule(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: SessionManagementService = Depends(get_service),
):
    return await _run_dashboard_json(
        request,
        service.update_session_rule,
        label="Falha ao atualizar as regras da sessão",
    )


@legacy_router.post("/delete-rule")
async def delete_dashboard_session_rule(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: SessionManagementService = Depends(get_service),
):
    return await _run_dashboard_json(
        request,
        service.delete_session_rule,
        label="Falha ao excluir as regras da sessão",
    )


@legacy_router.post("/batch-delete-rule")
async def batch_delete_dashboard_session_rule(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: SessionManagementService = Depends(get_service),
):
    return await _run_dashboard_json(
        request,
        service.batch_delete_session_rule,
        label="Falha ao excluir as regras das sessões em lote",
    )


@legacy_router.get("/active-umos")
async def list_dashboard_active_umos(
    _username: str = Depends(require_dashboard_user),
    service: SessionManagementService = Depends(get_service),
):
    return await _run(service.list_active_umos, label="Falha ao obter a lista de UMO")


@legacy_router.get("/list-all-with-status")
async def list_dashboard_umos_with_status(
    page: int = Query(1),
    page_size: int = Query(20),
    search: str = Query(""),
    message_type: str = Query("all"),
    platform: str = Query(""),
    _username: str = Depends(require_dashboard_user),
    service: SessionManagementService = Depends(get_service),
):
    return await _run(
        lambda: service.list_all_umos_with_status(
            page=page,
            page_size=page_size,
            search=search.strip(),
            message_type=message_type,
            platform=platform,
        ),
        label="Falha ao obter os estados das sessões",
    )


@legacy_router.post("/batch-update-service")
async def batch_update_dashboard_session_service(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: SessionManagementService = Depends(get_service),
):
    return await _run_dashboard_json(
        request,
        service.batch_update_service,
        label="Falha ao atualizar os estados dos serviços em lote",
    )


@legacy_router.post("/batch-update-provider")
async def batch_update_dashboard_session_provider(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: SessionManagementService = Depends(get_service),
):
    return await _run_dashboard_json(
        request,
        service.batch_update_provider,
        label="Falha ao atualizar provedores em lote",
    )


@legacy_router.get("/groups")
async def list_dashboard_session_groups(
    _username: str = Depends(require_dashboard_user),
    service: SessionManagementService = Depends(get_service),
):
    return await _run(service.list_groups, label="Falha ao obter os grupos")


@legacy_router.post("/group/create")
async def create_dashboard_session_group(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: SessionManagementService = Depends(get_service),
):
    return await _run_dashboard_json(
        request,
        service.create_group,
        label="Falha ao criar o grupo",
    )


@legacy_router.post("/group/update")
async def update_dashboard_session_group(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: SessionManagementService = Depends(get_service),
):
    return await _run_dashboard_json(
        request,
        service.update_group,
        label="Falha ao atualizar o grupo",
    )


@legacy_router.post("/group/delete")
async def delete_dashboard_session_group(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: SessionManagementService = Depends(get_service),
):
    return await _run_dashboard_json(
        request,
        service.delete_group,
        label="Falha ao excluir o grupo",
    )
