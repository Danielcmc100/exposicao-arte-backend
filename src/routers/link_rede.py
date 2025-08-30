from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from models.link_rede import LinkRedeCreate, LinkRedeDB, LinkRedeResponse
from repositories.link_rede import (
    adicionar_link_rede,
    atualizar_link_rede,
    buscar_link_rede_por_id,
    buscar_links_rede,
    remover_link_rede,
)

rota = APIRouter(prefix="/links_rede", tags=["links_rede"])


SessionInjetada = Annotated[Session, Depends(get_session)]


@rota.get("/")
def obter_links_rede(session: SessionInjetada) -> list[LinkRedeResponse]:
    links_rede_list = buscar_links_rede(session)
    return list(map(LinkRedeResponse.model_validate, links_rede_list))


@rota.get("/{link_rede_id}")
def ler_link_rede(link_rede_id: int, session: SessionInjetada) -> LinkRedeResponse | None:
    link_rede = buscar_link_rede_por_id(link_rede_id, session)
    return LinkRedeResponse.model_validate(link_rede) if link_rede else None


@rota.post("/")
def criar_link_rede(link_rede: LinkRedeCreate, session: SessionInjetada) -> LinkRedeResponse:
    link_rede_db = LinkRedeDB.model_validate(link_rede)
    return LinkRedeResponse.model_validate(adicionar_link_rede(link_rede_db, session))


@rota.put("/{link_rede_id}")
def atualizar_link_rede(
    link_rede_id: int, link_rede: LinkRedeCreate, session: SessionInjetada
) -> LinkRedeResponse | None:
    link_rede_db = LinkRedeDB.model_validate(link_rede)
    link_rede_atualizado = atualizar_link_rede(link_rede_id, link_rede_db, session)
    return LinkRedeResponse.model_validate(link_rede_atualizado)


@rota.delete("/{link_rede_id}")
def excluir_link_rede(
    link_rede_id: int, session: SessionInjetada
) -> LinkRedeResponse | None:
    link_rede_removido = remover_link_rede(link_rede_id, session)
    return LinkRedeResponse.model_validate(link_rede_removido)
