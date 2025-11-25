"""Repositório para operações de avaliações obras."""

from collections.abc import Sequence

from sqlmodel import Session, select

from models.avaliacoes_obras import AvaliacaoObraDB


def buscar_avaliacao_obra(
    session: Session,
) -> Sequence[AvaliacaoObraDB]:
    """Retorna todas as avaliações obras.

    Args:
        session: Sessão do banco de dados.

    Returns:
        Sequence[AvaliacaoObraDB]: Lista de avaliações obras.

    """
    return session.exec(select(AvaliacaoObraDB)).all()


def buscar_avaliacao_obra_por_id(
    avaliacao_obra_id: int, session: Session
) -> AvaliacaoObraDB | None:
    """Busca umaAvaliacao Obrapelo ID.

    Args:
        avaliacao_obra_id: ID da obra.
        session: Sessão do banco de dados.

    Returns:
        AvaliacaoObraDB | None:Avaliacao Obraencontrada ou None.

    """
    return session.get(AvaliacaoObraDB, avaliacao_obra_id)


def adicionar_avaliacao_obra(
    avaliacao_obra: AvaliacaoObraDB, session: Session
) -> AvaliacaoObraDB:
    """Adiciona uma nova obra.

    Args:
        avaliacao_obra: Dados daAvaliacao Obraa ser adicionada.
        session: Sessão do banco de dados.

    Returns:
        AvaliacaoObraDB:Avaliacao Obraadicionada.

    """
    session.add(avaliacao_obra)
    session.commit()
    session.refresh(avaliacao_obra)
    return avaliacao_obra


def atualizar_avaliacao_obra_bd(
    avaliacao_obra_id: int, obra: AvaliacaoObraDB, session: Session
) -> AvaliacaoObraDB | None:
    """Atualiza umaAvaliacao Obraexistente.

    Args:
        avaliacao_obra_id: ID daAvaliacao Obraa ser atualizada.
        obra: Novos dados da obra.
        session: Sessão do banco de dados.

    Returns:
        AvaliacaoObraDB | None:Avaliacao Obraatualizada ou None.

    """
    avaliacao_obra_existente = session.get(AvaliacaoObraDB, avaliacao_obra_id)
    if not avaliacao_obra_existente:
        return None

    for field, value in obra.model_dump().items():
        setattr(avaliacao_obra_existente, field, value)

    session.commit()
    session.refresh(avaliacao_obra_existente)
    return avaliacao_obra_existente


def remover_avaliacao_obra(
    avaliacao_obra_id: int, session: Session
) -> AvaliacaoObraDB | None:
    """Remove uma obra.

    Args:
        avaliacao_obra_id: ID daAvaliacao Obraa ser removida.
        session: Sessão do banco de dados.

    Returns:
        AvaliacaoObraDB | None:Avaliacao Obraremovida ou None.

    """
    obra_existente = buscar_avaliacao_obra_por_id(avaliacao_obra_id, session)
    if not obra_existente:
        return None
    session.delete(obra_existente)
    session.commit()
    return obra_existente
