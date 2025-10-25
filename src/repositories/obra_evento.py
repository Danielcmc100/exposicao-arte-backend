"""Repositório para operações de associação entre obras e eventos."""

from sqlmodel import Session, select

from models.obra_evento import ObraEventoDB


def adicionar_obra_ao_evento(
    session: Session, obra_evento: ObraEventoDB
) -> ObraEventoDB:
    """Adiciona uma obra a um evento.

    Returns:
        ObraEventoDB: Associação criada entre obra e evento.

    """
    session.add(obra_evento)
    session.commit()
    session.refresh(obra_evento)
    return obra_evento


def remover_obra_do_evento(
    session: Session, obra_evento: ObraEventoDB
) -> bool:
    """Remove uma obra de um evento.

    Returns:
        bool: True se removido com sucesso, False caso contrário.

    """
    statement = select(ObraEventoDB).where(
        ObraEventoDB.id_obra == obra_evento.id_obra,
        ObraEventoDB.id_evento == obra_evento.id_evento,
    )

    obra_evento_retornado = session.exec(statement).one_or_none()

    if obra_evento_retornado:
        session.delete(obra_evento_retornado)
        session.commit()
        return True
    return False
