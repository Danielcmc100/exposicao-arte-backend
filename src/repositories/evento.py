"""Repositório para operações de eventos."""

from collections.abc import Sequence

from sqlmodel import Session, select

from models.evento import EventoDB
from models.obra import ObraDB


def buscar_eventos(session: Session) -> Sequence[EventoDB]:
    """Retorna todos os eventos.

    Args:
        session: Sessão do banco de dados.

    Returns:
        Sequence[EventoDB]: Lista de eventos.

    """
    return session.exec(select(EventoDB)).all()


def buscar_evento_por_id(evento_id: int, session: Session) -> EventoDB | None:
    """Busca um evento pelo ID.

    Args:
        evento_id: ID do evento.
        session: Sessão do banco de dados.

    Returns:
        EventoDB | None: Evento encontrado ou None.

    """
    return session.get(EventoDB, evento_id)


def adicionar_evento(evento: EventoDB, session: Session) -> EventoDB:
    """Adiciona um novo evento.

    Args:
        evento: Dados do evento a ser adicionado.
        session: Sessão do banco de dados.

    Returns:
        EventoDB: Evento adicionado.

    """
    session.add(evento)
    session.commit()
    session.refresh(evento)
    return evento


def atualizar_evento_bd(
    evento_id: int, evento: EventoDB, session: Session
) -> EventoDB | None:
    """Atualiza um evento existente.

    Args:
        evento_id: ID do evento a ser atualizado.
        evento: Novos dados do evento.
        session: Sessão do banco de dados.

    Returns:
        EventoDB | None: Evento atualizado ou None.

    """
    evento_existente = session.get(EventoDB, evento_id)
    if not evento_existente:
        return None
    evento_existente.nome = evento.nome
    evento_existente.data = evento.data
    evento_existente.local = evento.local
    evento_existente.endereco = evento.endereco
    evento_existente.id_organizador = evento.id_organizador
    evento_existente.id_responsavel = evento.id_responsavel
    session.commit()
    session.refresh(evento_existente)
    return evento_existente


def remover_evento(evento_id: int, session: Session) -> EventoDB | None:
    """Remove um evento.

    Args:
        evento_id: ID do evento a ser removido.
        session: Sessão do banco de dados.

    Returns:
        EventoDB | None: Evento removido ou None.

    """
    evento_existente = buscar_evento_por_id(evento_id, session)
    if not evento_existente:
        return None
    session.delete(evento_existente)
    session.commit()
    return evento_existente


def buscar_eventos_por_obra(
    obra_id: int, session: Session
) -> Sequence[EventoDB]:
    """Retorna todos os eventos de uma obra específica.

    Args:
        obra_id: ID da obra.
        session: Sessão do banco de dados.

    Returns:
        Sequence[EventoDB]: Lista de eventos da obra.

    """
    obra_existente = session.get(ObraDB, obra_id)
    if not obra_existente:
        return []

    return obra_existente.eventos
