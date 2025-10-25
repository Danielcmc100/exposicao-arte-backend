"""Rotas para gerenciamento de avaliações de eventos."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from models.avaliacoes_eventos import (
    AvaliacaoEventoCreate,
    AvaliacaoEventoDB,
    AvaliacaoEventoResponse,
)
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
def obter_avaliacoes(
    session: SessionInjetada,
) -> list[AvaliacaoEventoResponse]:
    """Recupera todas as avaliações de eventos do banco de dados.

    Returns:
        list[AvaliacaoEventoResponse]: Lista de avaliações.

    """
    avaliacoes_list = buscar_avaliacoes(session)
    return list(map(AvaliacaoEventoResponse.model_validate, avaliacoes_list))


@rota.get("/{avaliacao_id}")
def ler_avaliacao(
    avaliacao_id: int, session: SessionInjetada
) -> AvaliacaoEventoResponse | None:
    """Recupera uma avaliação específica pelo seu ID.

    Returns:
        AvaliacaoEventoResponse | None: Avaliação encontrada ou None.

    """
    avaliacao = buscar_avaliacao_por_id(avaliacao_id, session)
    return (
        AvaliacaoEventoResponse.model_validate(avaliacao)
        if avaliacao
        else None
    )


@rota.get("/evento/{evento_id}")
def obter_avaliacoes_por_evento(
    evento_id: int, session: SessionInjetada
) -> list[AvaliacaoEventoResponse]:
    """Recupera todas as avaliações de um evento específico.

    Returns:
        list[AvaliacaoEventoResponse]: Lista de avaliações do evento.

    """
    avaliacoes_list = buscar_avaliacoes_por_evento(evento_id, session)
    return list(map(AvaliacaoEventoResponse.model_validate, avaliacoes_list))


@rota.get("/usuario/{usuario_id}")
def obter_avaliacoes_por_usuario(
    usuario_id: int, session: SessionInjetada
) -> list[AvaliacaoEventoResponse]:
    """Recupera todas as avaliações de um usuário específico.

    Returns:
        list[AvaliacaoEventoResponse]: Lista de avaliações do usuário.

    """
    avaliacoes_list = buscar_avaliacoes_por_usuario(usuario_id, session)
    return list(map(AvaliacaoEventoResponse.model_validate, avaliacoes_list))


@rota.post("/")
def criar_avaliacao(
    avaliacao: AvaliacaoEventoCreate, session: SessionInjetada
) -> AvaliacaoEventoResponse:
    """Cria uma nova avaliação de evento no banco de dados.

    Returns:
        AvaliacaoEventoResponse: Dados da avaliação criada.

    """
    avaliacao_db = AvaliacaoEventoDB.model_validate(avaliacao)
    return AvaliacaoEventoResponse.model_validate(
        adicionar_avaliacao(avaliacao_db, session)
    )


@rota.put("/{avaliacao_id}")
def atualizar_avaliacao_router(
    avaliacao_id: int,
    avaliacao: AvaliacaoEventoCreate,
    session: SessionInjetada,
) -> AvaliacaoEventoResponse | None:
    """Atualiza os dados de uma avaliação existente.

    Returns:
        AvaliacaoEventoResponse | None: Avaliação atualizada ou None.

    """
    avaliacao_db = AvaliacaoEventoDB.model_validate(avaliacao)
    avaliacao_atualizada = atualizar_avaliacao(
        avaliacao_id, avaliacao_db, session
    )
    return (
        AvaliacaoEventoResponse.model_validate(avaliacao_atualizada)
        if avaliacao_atualizada
        else None
    )


@rota.delete("/{avaliacao_id}")
def excluir_avaliacao(
    avaliacao_id: int, session: SessionInjetada
) -> AvaliacaoEventoResponse | None:
    """Remove uma avaliação do banco de dados.

    Returns:
        AvaliacaoEventoResponse | None: Avaliação removida ou None.

    """
    avaliacao_removida = remover_avaliacao(avaliacao_id, session)
    return (
        AvaliacaoEventoResponse.model_validate(avaliacao_removida)
        if avaliacao_removida
        else None
    )
