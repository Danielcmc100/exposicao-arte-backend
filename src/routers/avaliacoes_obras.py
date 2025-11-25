"""Rotas para gerenciamento de avaliações de obras."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from models.avaliacoes_obras import (
    AvaliacaoObraCreate,
    AvaliacaoObraDB,
    AvaliacaoObraResponse,
)
from repositories.avaliacoes_obras import (
    adicionar_avaliacao_obra,
    atualizar_avaliacao_obra_bd,
    buscar_avaliacao_obra,
    buscar_avaliacao_obra_por_id,
    remover_avaliacao_obra,
)

rota = APIRouter(prefix="/avaliacoe_obras", tags=["avaliacoe_obras"])

SessionInjetada = Annotated[Session, Depends(get_session)]


@rota.get("/")
def obter_avaliacoes(
    session: SessionInjetada,
) -> list[AvaliacaoObraResponse]:
    """Recupera todas as avaliações de obras do banco de dados.

    Returns:
        list[AvaliacaoObraResponse]: Lista de avaliações.

    """
    avaliacoes_list = buscar_avaliacao_obra(session)
    return list(map(AvaliacaoObraResponse.model_validate, avaliacoes_list))


@rota.get("/{avaliacao_id}")
def ler_avaliacao(
    avaliacao_id: int, session: SessionInjetada
) -> AvaliacaoObraResponse | None:
    """Recupera uma avaliação específica pelo seu ID.

    Returns:
        AvaliacaoObraResponse | None: Avaliação encontrada ou None.

    """
    avaliacao = buscar_avaliacao_obra_por_id(avaliacao_id, session)
    return (
        AvaliacaoObraResponse.model_validate(avaliacao) if avaliacao else None
    )


# @rota.get("/evento/{evento_id}")
# def obter_avaliacoes_por_evento(
#     evento_id: int, session: SessionInjetada
# ) -> list[AvaliacaoObraResponse]:
#     """Recupera todas as avaliações de um evento específico.

#     Returns:
#         list[AvaliacaoObraResponse]: Lista de avaliações do evento.

#     """
#     avaliacoes_list = buscar_avaliacoes_por_evento(evento_id, session)
#     return list(map(AvaliacaoObraResponse.model_validate, avaliacoes_list))


# @rota.get("/usuario/{usuario_id}")
# def obter_avaliacoes_por_usuario(
#     usuario_id: int, session: SessionInjetada
# ) -> list[AvaliacaoObraResponse]:
#     """Recupera todas as avaliações de um usuário específico.

#     Returns:
#         list[AvaliacaoObraResponse]: Lista de avaliações do usuário.

#     """
#     avaliacoes_list = buscar_avaliacoes_por_usuario(usuario_id, session)
#     return list(map(AvaliacaoObraResponse.model_validate, avaliacoes_list))


@rota.post("/")
def criar_avaliacao(
    avaliacao: AvaliacaoObraCreate, session: SessionInjetada
) -> AvaliacaoObraResponse:
    """Cria uma nova avaliação de evento no banco de dados.

    Returns:
        AvaliacaoObraResponse: Dados da avaliação criada.

    """
    avaliacao_db = AvaliacaoObraDB.model_validate(avaliacao)
    return AvaliacaoObraResponse.model_validate(
        adicionar_avaliacao_obra(avaliacao_db, session)
    )


@rota.put("/{avaliacao_id}")
def atualizar_avaliacao_router(
    avaliacao_id: int,
    avaliacao: AvaliacaoObraCreate,
    session: SessionInjetada,
) -> AvaliacaoObraResponse | None:
    """Atualiza os dados de uma avaliação existente.

    Returns:
        AvaliacaoObraResponse | None: Avaliação atualizada ou None.

    """
    avaliacao_db = AvaliacaoObraDB.model_validate(avaliacao)
    avaliacao_atualizada = atualizar_avaliacao_obra_bd(
        avaliacao_id, avaliacao_db, session
    )
    return (
        AvaliacaoObraResponse.model_validate(avaliacao_atualizada)
        if avaliacao_atualizada
        else None
    )


@rota.delete("/{avaliacao_id}")
def excluir_avaliacao(
    avaliacao_id: int, session: SessionInjetada
) -> AvaliacaoObraResponse | None:
    """Remove uma avaliação do banco de dados.

    Returns:
        AvaliacaoObraResponse | None: Avaliação removida ou None.

    """
    avaliacao_removida = remover_avaliacao_obra(avaliacao_id, session)
    return (
        AvaliacaoObraResponse.model_validate(avaliacao_removida)
        if avaliacao_removida
        else None
    )
