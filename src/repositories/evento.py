from typing import Sequence

from sqlmodel import Session, select

from models.evento import EventoDB


def buscar_eventos(session: Session) -> Sequence[EventoDB]:
    return session.exec(select(EventoDB)).all()


def buscar_evento_por_id(evento_id: int, session: Session) -> EventoDB | None:
    return session.get(EventoDB, evento_id)


def adicionar_evento(evento: EventoDB, session: Session) -> EventoDB:
    session.add(evento)
    session.commit()
    session.refresh(evento)
    return evento


def atualizar_evento(evento_id: int, evento: EventoDB, session: Session) -> EventoDB | None:
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
    evento_existente = buscar_evento_por_id(evento_id, session)
    if not evento_existente:
        return None
    session.delete(evento_existente)
    session.commit()
    return evento_existente



def remover_evento(evento_id: int, session: Session) -> EventoDB | None:
    evento_existente = buscar_evento_por_id(evento_id, session)
    if not evento_existente:
        return None
    session.delete(evento_existente)
    session.commit()
    return evento_existente
