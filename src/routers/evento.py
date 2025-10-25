"""Rotas para gerenciamento de eventos."""

from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from models.evento import EventoCreate, EventoDB, EventoResponse
from repositories.evento import (
    adicionar_evento,
    atualizar_evento_bd,
    buscar_evento_por_id,
    buscar_eventos,
    buscar_eventos_por_obra,
    remover_evento,
)

rota = APIRouter(prefix="/eventos", tags=["eventos"])

SessionInjetada = Annotated[Session, Depends(get_session)]


@rota.get("/")
def obter_eventos(session: SessionInjetada) -> list[EventoResponse]:
    """Recupera todos os eventos do banco de dados.

    Returns:
        list[EventoResponse]: Lista de eventos.

    """
    eventos_list = buscar_eventos(session)
    return list(map(EventoResponse.model_validate, eventos_list))


@rota.get("/{evento_id}")
def ler_evento(
    evento_id: int, session: SessionInjetada
) -> EventoResponse | None:
    """Recupera um evento específico pelo seu ID.

    Returns:
        EventoResponse | None: Evento encontrado ou None se não existir.

    """
    evento = buscar_evento_por_id(evento_id, session)
    return EventoResponse.model_validate(evento) if evento else None


@rota.post("/")
def criar_evento(
    evento: EventoCreate, session: SessionInjetada
) -> EventoResponse:
    """Cria um novo evento no banco de dados.

    Returns:
        EventoResponse: Dados do evento criado.

    """
    evento_db = EventoDB.model_validate(evento)
    return EventoResponse.model_validate(adicionar_evento(evento_db, session))


@rota.put("/{evento_id}")
def atualizar_evento(
    evento_id: int, evento: EventoCreate, session: SessionInjetada
) -> EventoResponse | None:
    """Atualiza os dados de um evento existente.

    Returns:
        EventoResponse | None: Evento atualizado ou None se não existir.

    """
    evento_db = EventoDB.model_validate(evento)
    evento_atualizado = atualizar_evento_bd(evento_id, evento_db, session)
    return EventoResponse.model_validate(evento_atualizado)


@rota.delete("/{evento_id}")
def excluir_evento(
    evento_id: int, session: SessionInjetada
) -> EventoResponse | None:
    """Remove um evento do banco de dados.

    Returns:
        EventoResponse | None: Evento removido ou None se não existir.

    """
    evento_removido = remover_evento(evento_id, session)
    return EventoResponse.model_validate(evento_removido)


@rota.get("/obra/{obra_id}")
def obter_eventos_por_obras(
    obra_id: int, session: SessionInjetada
) -> Sequence[EventoResponse]:
    """Recupera todos os eventos associados a uma obra específica.

    Returns:
        Sequence[EventoResponse]: Lista de eventos associados à obra.

    """
    obras_list = buscar_eventos_por_obra(obra_id, session)
    return list(map(EventoResponse.model_validate, obras_list))
