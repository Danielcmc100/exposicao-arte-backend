from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from models.comentario_obra import (
    ComentarioObraCreate,
    ComentarioObraDB,
    ComentarioObraResponse,
)
from repositories.comentario_obra import (
    adicionar_comentario_obra,
    atualizar_comentario_obra_bd,
    buscar_comentario_obra_por_id,
    buscar_comentarios_obras,
    remover_comentario_obra,
)

rota = APIRouter(prefix="/comentarios_obra", tags=["comentarios_obra"])


SessionInjetada = Annotated[Session, Depends(get_session)]


@rota.get("/")
def obter_comentarios_obras(session: SessionInjetada) -> list[ComentarioObraResponse]:
    comentarios_list = buscar_comentarios_obras(session)
    return list(map(ComentarioObraResponse.model_validate, comentarios_list))


@rota.get("/{comentario_obra_id}")
def ler_comentario_obra(
    comentario_obra_id: int, session: SessionInjetada
) -> ComentarioObraResponse | None:
    comentario_obra = buscar_comentario_obra_por_id(comentario_obra_id, session)
    return (
        ComentarioObraResponse.model_validate(comentario_obra)
        if comentario_obra
        else None
    )


@rota.post("/")
def criar_comentario_obra(
    comentario_obra: ComentarioObraCreate, session: SessionInjetada
) -> ComentarioObraResponse:
    comentario_obra_db = ComentarioObraDB.model_validate(comentario_obra)
    return ComentarioObraResponse.model_validate(
        adicionar_comentario_obra(comentario_obra_db, session)
    )


@rota.put("/{comentario_obra_id}")
def atualizar_comentario_obra(
    comentario_obra_id: int,
    comentario_obra: ComentarioObraCreate,
    session: SessionInjetada,
) -> ComentarioObraResponse | None:
    comentario_obra_db = ComentarioObraDB.model_validate(comentario_obra)
    comentario_obra_atualizado = atualizar_comentario_obra_bd(
        comentario_obra_id, comentario_obra_db, session
    )
    return (
        ComentarioObraResponse.model_validate(comentario_obra_atualizado)
        if comentario_obra_atualizado
        else None
    )


@rota.delete("/{comentario_obra_id}")
def excluir_comentario_obra(
    comentario_obra_id: int, session: SessionInjetada
) -> ComentarioObraResponse | None:
    comentario_obra_removido = remover_comentario_obra(comentario_obra_id, session)
    return ComentarioObraResponse.model_validate(comentario_obra_removido)
