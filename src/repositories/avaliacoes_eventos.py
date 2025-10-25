"""Repositório para operações de avaliações de eventos."""

from collections.abc import Sequence

from sqlmodel import Session, select

from models.avaliacoes_eventos import AvaliacaoEventoDB


def buscar_avaliacoes(session: Session) -> Sequence[AvaliacaoEventoDB]:
    """Retorna todas as avaliações.

    Returns:
        Sequence[AvaliacaoEventoDB]: Lista de todas as avaliações.

    """
    return session.exec(select(AvaliacaoEventoDB)).all()


def buscar_avaliacao_por_id(
    avaliacao_id: int, session: Session
) -> AvaliacaoEventoDB | None:
    """Busca uma avaliação pelo ID.

    Returns:
        AvaliacaoEventoDB | None: Avaliação encontrada ou None.

    """
    return session.get(AvaliacaoEventoDB, avaliacao_id)


def buscar_avaliacoes_por_evento(
    evento_id: int, session: Session
) -> Sequence[AvaliacaoEventoDB]:
    """Retorna todas as avaliações de um evento específico.

    Returns:
        Sequence[AvaliacaoEventoDB]: Lista de avaliações do evento.

    """
    return session.exec(
        select(AvaliacaoEventoDB).where(
            AvaliacaoEventoDB.evento_id == evento_id
        )
    ).all()


def buscar_avaliacoes_por_usuario(
    usuario_id: int, session: Session
) -> Sequence[AvaliacaoEventoDB]:
    """Retorna todas as avaliações feitas por um usuário específico.

    Returns:
        Sequence[AvaliacaoEventoDB]: Lista de avaliações do usuário.

    """
    return session.exec(
        select(AvaliacaoEventoDB).where(
            AvaliacaoEventoDB.usuario_id == usuario_id
        )
    ).all()


def adicionar_avaliacao(
    avaliacao: AvaliacaoEventoDB, session: Session
) -> AvaliacaoEventoDB:
    """Adiciona uma nova avaliação.

    Returns:
        AvaliacaoEventoDB: Avaliação criada.

    """
    session.add(avaliacao)
    session.commit()
    session.refresh(avaliacao)
    return avaliacao


def atualizar_avaliacao(
    avaliacao_id: int, avaliacao: AvaliacaoEventoDB, session: Session
) -> AvaliacaoEventoDB | None:
    """Atualiza os dados de uma avaliação existente.

    Returns:
        AvaliacaoEventoDB | None: Avaliação atualizada ou None.

    """
    avaliacao_existente = session.get(AvaliacaoEventoDB, avaliacao_id)
    if not avaliacao_existente:
        return None

    avaliacao_existente.gostou = avaliacao.gostou
    avaliacao_existente.avaliacao = avaliacao.avaliacao
    session.commit()
    session.refresh(avaliacao_existente)
    return avaliacao_existente


def remover_avaliacao(
    avaliacao_id: int, session: Session
) -> AvaliacaoEventoDB | None:
    """Remove uma avaliação.

    Returns:
        AvaliacaoEventoDB | None: Avaliação removida ou None.

    """
    avaliacao_existente = buscar_avaliacao_por_id(avaliacao_id, session)
    if not avaliacao_existente:
        return None
    session.delete(avaliacao_existente)
    session.commit()
    return avaliacao_existente
