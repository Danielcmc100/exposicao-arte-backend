"""Rotas para gerenciamento de obras de arte."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from database import get_session
from models.obra import ObraCreate, ObraDB, ObraResponse
from repositories.obra import (
    adicionar_obra,
    atualizar_obra_bd,
    buscar_obra_por_id,
    buscar_obras,
    buscar_obras_por_evento,
    remover_obra,
)

rota = APIRouter(prefix="/obras", tags=["obras"])


SessionInjetada = Annotated[Session, Depends(get_session)]


@rota.get("/")
def obter_obras(session: SessionInjetada) -> list[ObraResponse]:
    """Recupera todas as obras do banco de dados.

    Returns:
        list[ObraResponse]: Lista de obras.

    """
    obras_list = buscar_obras(session)
    return list(map(ObraResponse.model_validate, obras_list))


@rota.get("/{obra_id}")
def ler_obra(obra_id: int, session: SessionInjetada) -> ObraResponse | None:
    """Recupera uma obra específica pelo seu ID.

    Returns:
        ObraResponse | None: Obra encontrada ou None se não existir.

    """
    obra = buscar_obra_por_id(obra_id, session)
    return ObraResponse.model_validate(obra) if obra else None


@rota.post("/")
def criar_obra(obra: ObraCreate, session: SessionInjetada) -> ObraResponse:
    """Cria uma nova obra no banco de dados.

    Returns:
        ObraResponse: Dados da obra criada.

    """
    obra_db = ObraDB.model_validate(obra)
    return ObraResponse.model_validate(adicionar_obra(obra_db, session))


@rota.put("/{obra_id}")
def atualizar_obra(
    obra_id: int, obra: ObraCreate, session: SessionInjetada
) -> ObraResponse | None:
    """Atualiza os dados de uma obra existente.

    Returns:
        ObraResponse | None: Obra atualizada.

    Raises:
        HTTPException: Se a obra não for encontrada (status 404).

    """
    obra_db = ObraDB.model_validate(obra)
    obra_atualizada = atualizar_obra_bd(obra_id, obra_db, session)
    if not obra_atualizada:
        raise HTTPException(status_code=404, detail="Obra não encontrada")
    return ObraResponse.model_validate(obra_atualizada)


@rota.delete("/{obra_id}")
def excluir_obra(
    obra_id: int, session: SessionInjetada
) -> ObraResponse | None:
    """Remove uma obra do banco de dados.

    Returns:
        ObraResponse | None: Obra removida ou None se não existir.

    """
    categoria_removida = remover_obra(obra_id, session)
    return ObraResponse.model_validate(categoria_removida)


@rota.get("/evento/{evento_id}")
def obter_obras_por_evento(
    evento_id: int, session: SessionInjetada
) -> list[ObraResponse]:
    """Recupera todas as obras associadas a um evento específico.

    Returns:
        list[ObraResponse]: Lista de obras associadas ao evento.

    """
    obras_list = buscar_obras_por_evento(evento_id, session)
    return list(map(ObraResponse.model_validate, obras_list))
