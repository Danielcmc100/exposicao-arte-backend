"""Rotas para gerenciamento de comentários em eventos."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from models.comentario_evento import (
    ComentarioEventoCreate,
    ComentarioEventoDB,
    ComentarioEventoResponse,
)
from repositories.comentario_evento import (
    adicionar_comentario,
    atualizar_comentario,
    buscar_comentario_por_id,
    buscar_comentarios,
    buscar_comentarios_por_evento,
    buscar_comentarios_por_usuario,
    remover_comentario,
)

rota = APIRouter(prefix="/comentarios", tags=["comentarios"])

SessionInjetada = Annotated[Session, Depends(get_session)]


@rota.get("/")
def obter_comentarios(
    session: SessionInjetada,
) -> list[ComentarioEventoResponse]:
    """Recupera todos os comentários do banco de dados.

    Returns:
        list[ComentarioEventoResponse]: Lista de comentários.

    """
    comentarios_list = buscar_comentarios(session)
    return list(map(ComentarioEventoResponse.model_validate, comentarios_list))


@rota.get("/{comentario_id}")
def ler_comentario(
    comentario_id: int, session: SessionInjetada
) -> ComentarioEventoResponse | None:
    """Recupera um comentário específico pelo seu ID.

    Returns:
        ComentarioEventoResponse | None: Comentário encontrado ou None.

    """
    comentario = buscar_comentario_por_id(comentario_id, session)
    return (
        ComentarioEventoResponse.model_validate(comentario)
        if comentario
        else None
    )


@rota.get("/evento/{evento_id}")
def obter_comentarios_por_evento(
    evento_id: int, session: SessionInjetada
) -> list[ComentarioEventoResponse]:
    """Recupera todos os comentários de um evento específico.

    Returns:
        list[ComentarioEventoResponse]: Lista de comentários do evento.

    """
    comentarios_list = buscar_comentarios_por_evento(evento_id, session)
    return list(map(ComentarioEventoResponse.model_validate, comentarios_list))


@rota.get("/usuario/{usuario_id}")
def obter_comentarios_por_usuario(
    usuario_id: int, session: SessionInjetada
) -> list[ComentarioEventoResponse]:
    """Recupera todos os comentários de um usuário específico.

    Returns:
        list[ComentarioEventoResponse]: Lista de comentários do usuário.

    """
    comentarios_list = buscar_comentarios_por_usuario(usuario_id, session)
    return list(map(ComentarioEventoResponse.model_validate, comentarios_list))


@rota.post("/")
def criar_comentario(
    comentario: ComentarioEventoCreate, session: SessionInjetada
) -> ComentarioEventoResponse:
    """Cria um novo comentário no banco de dados.

    Returns:
        ComentarioEventoResponse: Dados do comentário criado.

    """
    comentario_db = ComentarioEventoDB.model_validate(comentario)
    return ComentarioEventoResponse.model_validate(
        adicionar_comentario(comentario_db, session)
    )


@rota.put("/{comentario_id}")
def atualizar_comentario_router(
    comentario_id: int,
    comentario: ComentarioEventoCreate,
    session: SessionInjetada,
) -> ComentarioEventoResponse | None:
    """Atualiza os dados de um comentário existente.

    Returns:
        ComentarioEventoResponse | None: Comentário atualizado ou None.

    """
    comentario_db = ComentarioEventoDB.model_validate(comentario)
    comentario_atualizado = atualizar_comentario(
        comentario_id, comentario_db, session
    )
    return ComentarioEventoResponse.model_validate(comentario_atualizado)


@rota.delete("/{comentario_id}")
def excluir_comentario(
    comentario_id: int, session: SessionInjetada
) -> ComentarioEventoResponse | None:
    """Remove um comentário do banco de dados.

    Returns:
        ComentarioEventoResponse | None: Comentário removido ou None.

    """
    comentario_removido = remover_comentario(comentario_id, session)
    return ComentarioEventoResponse.model_validate(comentario_removido)
