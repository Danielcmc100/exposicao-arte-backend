"""Rotas para gerenciamento de associações entre obras e eventos."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from database import get_session
from models import ObraEventoDB
from repositories.obra_evento import (
    adicionar_obra_ao_evento,
    remover_obra_do_evento,
)

rota = APIRouter(prefix="/obras-evento", tags=["obras eventos"])


SessionInjetada = Annotated[Session, Depends(get_session)]


@rota.post("/")
def criar_obra_evento(
    obra: ObraEventoDB, session: SessionInjetada
) -> ObraEventoDB:
    """Associa uma obra a um evento.

    Returns:
        ObraEventoDB: Dados da associação criada.

    """
    return adicionar_obra_ao_evento(session, obra)


@rota.delete("/{obra_id}", status_code=204)
def excluir_obra(obra: ObraEventoDB, session: SessionInjetada) -> None:
    """Remove a associação de uma obra com um evento.

    Raises:
        HTTPException: Se a obra não for encontrada no evento (status 404).

    """
    obra_removida = remover_obra_do_evento(session, obra)
    if not obra_removida:
        raise HTTPException(
            status_code=404, detail="Obra não encontrada no evento"
        )
