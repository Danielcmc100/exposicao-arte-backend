from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from models.avaliacoes_eventos import (
    AvaliacaoEventoCreate,
    AvaliacaoEventoDB,
    AvaliacaoEventoResponse,
)

from models.comentario_evento import ComentarioEventoResponse
from repositories.avaliacoes_eventos import (
    adicionar_avaliacao,
    atualizar_avaliacao,
    buscar_avaliacao_por_id,
    buscar_avaliacoes,
    buscar_avaliacoes_por_evento,
    buscar_avaliacoes_por_usuario,
    remover_avaliacao,
)

rota = APIRouter(prefix="/avaliacoes", tags=["avaliacoes"])

SessionInjetada = Annotated[Session, Depends(get_session)]


@rota.get("/")
def obter_avaliacoes(session: SessionInjetada) -> list[AvaliacaoEventoResponse]:
    avaliacoes_list = buscar_avaliacoes(session)
    return list(map(AvaliacaoEventoResponse.model_validate, avaliacoes_list))


@rota.get("/{avaliacao_id}")
def ler_avaliacao(
    avaliacao_id: int, session: SessionInjetada
) -> AvaliacaoEventoResponse | None:
    avaliacao = buscar_avaliacao_por_id(avaliacao_id, session)
    return AvaliacaoEventoResponse.model_validate(avaliacao) if avaliacao else None


@rota.get("/evento/{evento_id}")
def obter_avaliacoes_por_evento(
    evento_id: int, session: SessionInjetada
) -> list[AvaliacaoEventoResponse]:
    avaliacoes_list = buscar_avaliacoes_por_evento(evento_id, session)
    return list(map(AvaliacaoEventoResponse.model_validate, avaliacoes_list))


@rota.get("/usuario/{usuario_id}")
def obter_avaliacoes_por_usuario(
    usuario_id: int, session: SessionInjetada
) -> list[AvaliacaoEventoResponse]:
    avaliacoes_list = buscar_avaliacoes_por_usuario(usuario_id, session)
    return list(map(AvaliacaoEventoResponse.model_validate, avaliacoes_list))


@rota.post("/")
def criar_avaliacao(
    avaliacao: AvaliacaoEventoCreate, session: SessionInjetada
) -> AvaliacaoEventoResponse:
    avaliacao_db = AvaliacaoEventoDB.model_validate(avaliacao)
    return AvaliacaoEventoResponse.model_validate(
        adicionar_avaliacao(avaliacao_db, session)
    )


@rota.put("/{avaliacao_id}")
def atualizar_avaliacao_router(
    avaliacao_id: int, avaliacao: AvaliacaoEventoCreate, session: SessionInjetada
) -> AvaliacaoEventoResponse | None:
    avaliacao_db = AvaliacaoEventoDB.model_validate(avaliacao)
    avaliacao_atualizada = atualizar_avaliacao(avaliacao_id, avaliacao_db, session)
    return AvaliacaoEventoResponse.model_validate(avaliacao_atualizada) if avaliacao_atualizada else None


@rota.delete("/{avaliacao_id}")
def excluir_avaliacao(
    avaliacao_id: int, session: SessionInjetada
) -> AvaliacaoEventoResponse | None:
    avaliacao_removida = remover_avaliacao(avaliacao_id, session)
    return AvaliacaoEventoResponse.model_validate(avaliacao_removida) if avaliacao_removida else None
