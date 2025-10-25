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
    obras_list = buscar_obras(session)
    return list(map(ObraResponse.model_validate, obras_list))


@rota.get("/{obra_id}")
def ler_obra(obra_id: int, session: SessionInjetada) -> ObraResponse | None:
    obra = buscar_obra_por_id(obra_id, session)
    return ObraResponse.model_validate(obra) if obra else None


@rota.post("/")
def criar_obra(obra: ObraCreate, session: SessionInjetada) -> ObraResponse:
    obra_db = ObraDB.model_validate(obra)
    return ObraResponse.model_validate(adicionar_obra(obra_db, session))


@rota.put("/{obra_id}")
def atualizar_obra(
    obra_id: int, obra: ObraCreate, session: SessionInjetada
) -> ObraResponse | None:
    obra_db = ObraDB.model_validate(obra)
    obra_atualizada = atualizar_obra_bd(obra_id, obra_db, session)
    if not obra_atualizada:
        raise HTTPException(status_code=404, detail="Obra não encontrada")
    return ObraResponse.model_validate(obra_atualizada)


@rota.delete("/{obra_id}")
def excluir_obra(
    obra_id: int, session: SessionInjetada
) -> ObraResponse | None:
    categoria_removida = remover_obra(obra_id, session)
    return ObraResponse.model_validate(categoria_removida)


@rota.get("/evento/{evento_id}")
def obter_obras_por_evento(
    evento_id: int, session: SessionInjetada
) -> list[ObraResponse]:
    obras_list = buscar_obras_por_evento(evento_id, session)
    return list(map(ObraResponse.model_validate, obras_list))
