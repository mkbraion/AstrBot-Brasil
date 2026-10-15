from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, Depends, Request

from astrbot.core import logger
from astrbot.dashboard.async_utils import run_maybe_async
from astrbot.dashboard.responses import error, ok
from astrbot.dashboard.schemas import (
    KnowledgeBaseCreateRequest,
    KnowledgeBaseImportRequest,
    KnowledgeBaseRequest,
    KnowledgeBaseRetrieveRequest,
    KnowledgeBaseUrlImportRequest,
)
from astrbot.dashboard.services.knowledge_base_service import (
    KnowledgeBaseService,
    KnowledgeBaseServiceError,
)

from .auth import AuthContext, require_dashboard_user, require_scope
from .multipart import multipart_parts

router = APIRouter(tags=["Knowledge Bases"])
legacy_router = APIRouter(
    prefix="/api/kb",
    tags=["Dashboard Knowledge Bases"],
    include_in_schema=False,
)


def get_service(request: Request) -> KnowledgeBaseService:
    return request.app.state.services.knowledge_bases


async def require_kb_scope(request: Request) -> AuthContext:
    return await require_scope(request, "kb")


async def _json_or_empty(request: Request) -> dict[str, Any]:
    try:
        data = await request.json()
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _to_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


async def _run(operation, *, prefix: str):
    try:
        result = await run_maybe_async(operation)
        if isinstance(result, tuple):
            data, message = result
            return ok(data, message)
        return ok(result)
    except (KnowledgeBaseServiceError, ValueError) as exc:
        return error(str(exc))
    except Exception as exc:
        logger.error("%s: %s", prefix, exc, exc_info=True)
        return error(f"{prefix}: {exc!s}")


async def _run_json(
    request: Request,
    operation: Callable[[dict[str, Any]], Any],
    *,
    prefix: str,
):
    body = await _json_or_empty(request)
    return await _run(lambda: operation(body), prefix=prefix)


@router.get("/knowledge-bases")
async def list_knowledge_bases(
    request: Request,
    _auth: AuthContext = Depends(require_kb_scope),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.list_kbs(
            page=_to_int(request.query_params.get("page"), 1),
            page_size=_to_int(request.query_params.get("page_size"), 20),
        ),
        prefix="Falha ao obter as bases de conhecimento",
    )


@router.post("/knowledge-bases")
async def create_knowledge_base(
    payload: KnowledgeBaseCreateRequest,
    _auth: AuthContext = Depends(require_kb_scope),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.create_kb(payload.canonical_payload()),
        prefix="Falha ao criar a base de conhecimento",
    )


@router.get("/knowledge-bases/tasks/{task_id}")
async def get_knowledge_base_task(
    task_id: str,
    _auth: AuthContext = Depends(require_kb_scope),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.get_upload_progress(task_id),
        prefix="Falha ao obter o progresso do envio",
    )


@router.get("/knowledge-bases/{kb_id}")
async def get_knowledge_base(
    kb_id: str,
    _auth: AuthContext = Depends(require_kb_scope),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.get_kb(kb_id),
        prefix="Falha ao obter os detalhes da base de conhecimento",
    )


@router.put("/knowledge-bases/{kb_id}")
async def update_knowledge_base(
    kb_id: str,
    payload: KnowledgeBaseRequest,
    _auth: AuthContext = Depends(require_kb_scope),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.update_kb({**payload.canonical_payload(), "kb_id": kb_id}),
        prefix="Falha ao atualizar a base de conhecimento",
    )


@router.delete("/knowledge-bases/{kb_id}")
async def delete_knowledge_base(
    kb_id: str,
    _auth: AuthContext = Depends(require_kb_scope),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.delete_kb({"kb_id": kb_id}),
        prefix="Falha ao excluir a base de conhecimento",
    )


@router.get("/knowledge-bases/{kb_id}/stats")
async def get_knowledge_base_stats(
    kb_id: str,
    _auth: AuthContext = Depends(require_kb_scope),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.get_kb_stats(kb_id),
        prefix="Falha ao obter as estatísticas da base de conhecimento",
    )


@router.get("/knowledge-bases/{kb_id}/documents")
async def list_knowledge_base_documents(
    kb_id: str,
    request: Request,
    _auth: AuthContext = Depends(require_kb_scope),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.list_documents(
            kb_id=kb_id,
            page=_to_int(request.query_params.get("page"), 1),
            page_size=_to_int(request.query_params.get("page_size"), 100),
            search=request.query_params.get("search"),
        ),
        prefix="Falha ao obter os documentos",
    )


@router.post("/knowledge-bases/{kb_id}/documents")
async def upload_knowledge_base_document(
    kb_id: str,
    request: Request,
    _auth: AuthContext = Depends(require_kb_scope),
    service: KnowledgeBaseService = Depends(get_service),
):
    async def _operation():
        form_data, files = await multipart_parts(request, extra_form={"kb_id": kb_id})
        return await service.upload_document(
            content_type=request.headers.get("content-type"),
            form_data=form_data,
            files=files,
        )

    return await _run(_operation, prefix="Falha ao enviar o documento")


@router.post("/knowledge-bases/{kb_id}/documents/import")
async def import_knowledge_base_documents(
    kb_id: str,
    payload: KnowledgeBaseImportRequest,
    _auth: AuthContext = Depends(require_kb_scope),
    service: KnowledgeBaseService = Depends(get_service),
):
    body = payload.model_dump(exclude_none=True)
    return await _run(
        lambda: service.import_documents({"kb_id": kb_id, **body}),
        prefix="Falha ao importar o documento",
    )


@router.post("/knowledge-bases/{kb_id}/documents/import-url")
async def import_knowledge_base_document_url(
    kb_id: str,
    payload: KnowledgeBaseUrlImportRequest,
    _auth: AuthContext = Depends(require_kb_scope),
    service: KnowledgeBaseService = Depends(get_service),
):
    body = payload.model_dump(exclude_none=True)
    return await _run(
        lambda: service.upload_document_from_url({"kb_id": kb_id, **body}),
        prefix="Falha ao enviar o documento por URL",
    )


@router.get("/knowledge-bases/{kb_id}/documents/{document_id}")
async def get_knowledge_base_document(
    kb_id: str,
    document_id: str,
    _auth: AuthContext = Depends(require_kb_scope),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.get_document(kb_id=kb_id, doc_id=document_id),
        prefix="Falha ao obter os detalhes do documento",
    )


@router.delete("/knowledge-bases/{kb_id}/documents/{document_id}")
async def delete_knowledge_base_document(
    kb_id: str,
    document_id: str,
    _auth: AuthContext = Depends(require_kb_scope),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.delete_document({"kb_id": kb_id, "doc_id": document_id}),
        prefix="Falha ao excluir o documento",
    )


@router.get("/knowledge-bases/{kb_id}/chunks")
async def list_knowledge_base_chunks(
    kb_id: str,
    request: Request,
    _auth: AuthContext = Depends(require_kb_scope),
    service: KnowledgeBaseService = Depends(get_service),
):
    document_id = request.query_params.get("document_id") or request.query_params.get(
        "doc_id"
    )
    return await _run(
        lambda: service.list_chunks(
            kb_id=kb_id,
            doc_id=document_id,
            page=_to_int(request.query_params.get("page"), 1),
            page_size=_to_int(request.query_params.get("page_size"), 100),
        ),
        prefix="Falha ao obter os blocos de texto",
    )


@router.delete("/knowledge-bases/{kb_id}/chunks/{chunk_id}")
async def delete_knowledge_base_chunk(
    kb_id: str,
    chunk_id: str,
    request: Request,
    _auth: AuthContext = Depends(require_kb_scope),
    service: KnowledgeBaseService = Depends(get_service),
):
    document_id = request.query_params.get("document_id") or request.query_params.get(
        "doc_id"
    )
    return await _run(
        lambda: service.delete_chunk(
            {"kb_id": kb_id, "chunk_id": chunk_id, "doc_id": document_id}
        ),
        prefix="Falha ao excluir o bloco de texto",
    )


@router.post("/knowledge-bases/{kb_id}/retrieve")
async def retrieve_knowledge_base(
    kb_id: str,
    payload: KnowledgeBaseRetrieveRequest,
    _auth: AuthContext = Depends(require_kb_scope),
    service: KnowledgeBaseService = Depends(get_service),
):
    body = payload.model_dump(exclude_none=True)
    return await _run(
        lambda: service.retrieve({"kb_id": kb_id, **body}),
        prefix="Falha na busca",
    )


@legacy_router.get("/list")
async def dashboard_list_kbs(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.list_kbs(
            page=_to_int(request.query_params.get("page"), 1),
            page_size=_to_int(request.query_params.get("page_size"), 20),
        ),
        prefix="Falha ao obter as bases de conhecimento",
    )


@legacy_router.post("/create")
async def dashboard_create_kb(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run_json(
        request, service.create_kb, prefix="Falha ao criar a base de conhecimento"
    )


@legacy_router.get("/get")
async def dashboard_get_kb(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.get_kb(request.query_params.get("kb_id")),
        prefix="Falha ao obter os detalhes da base de conhecimento",
    )


@legacy_router.post("/update")
async def dashboard_update_kb(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run_json(
        request, service.update_kb, prefix="Falha ao atualizar a base de conhecimento"
    )


@legacy_router.post("/delete")
async def dashboard_delete_kb(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run_json(
        request, service.delete_kb, prefix="Falha ao excluir a base de conhecimento"
    )


@legacy_router.get("/stats")
async def dashboard_get_kb_stats(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.get_kb_stats(request.query_params.get("kb_id")),
        prefix="Falha ao obter as estatísticas da base de conhecimento",
    )


@legacy_router.get("/document/list")
async def dashboard_list_documents(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.list_documents(
            kb_id=request.query_params.get("kb_id"),
            page=_to_int(request.query_params.get("page"), 1),
            page_size=_to_int(request.query_params.get("page_size"), 100),
            search=request.query_params.get("search"),
        ),
        prefix="Falha ao obter os documentos",
    )


@legacy_router.post("/document/upload")
async def dashboard_upload_document(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: KnowledgeBaseService = Depends(get_service),
):
    async def _operation():
        form_data, files = await multipart_parts(request)
        return await service.upload_document(
            content_type=request.headers.get("content-type"),
            form_data=form_data,
            files=files,
        )

    return await _run(_operation, prefix="Falha ao enviar o documento")


@legacy_router.post("/document/import")
async def dashboard_import_documents(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run_json(
        request, service.import_documents, prefix="Falha ao importar o documento"
    )


@legacy_router.post("/document/upload/url")
async def dashboard_upload_document_from_url(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run_json(
        request,
        service.upload_document_from_url,
        prefix="Falha ao enviar o documento por URL",
    )


@legacy_router.get("/document/upload/progress")
async def dashboard_get_upload_progress(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.get_upload_progress(request.query_params.get("task_id")),
        prefix="Falha ao obter o progresso do envio",
    )


@legacy_router.get("/document/get")
async def dashboard_get_document(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.get_document(
            kb_id=request.query_params.get("kb_id"),
            doc_id=request.query_params.get("doc_id"),
        ),
        prefix="Falha ao obter os detalhes do documento",
    )


@legacy_router.post("/document/delete")
async def dashboard_delete_document(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run_json(
        request, service.delete_document, prefix="Falha ao excluir o documento"
    )


@legacy_router.get("/chunk/list")
async def dashboard_list_chunks(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run(
        lambda: service.list_chunks(
            kb_id=request.query_params.get("kb_id"),
            doc_id=request.query_params.get("doc_id"),
            page=_to_int(request.query_params.get("page"), 1),
            page_size=_to_int(request.query_params.get("page_size"), 100),
        ),
        prefix="Falha ao obter os blocos de texto",
    )


@legacy_router.post("/chunk/delete")
async def dashboard_delete_chunk(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run_json(
        request, service.delete_chunk, prefix="Falha ao excluir o bloco de texto"
    )


@legacy_router.post("/retrieve")
async def dashboard_retrieve(
    request: Request,
    _username: str = Depends(require_dashboard_user),
    service: KnowledgeBaseService = Depends(get_service),
):
    return await _run_json(request, service.retrieve, prefix="Falha na busca")
