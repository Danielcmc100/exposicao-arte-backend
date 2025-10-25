from collections.abc import Sequence

from sqlmodel import Session, select

from models.evento import EventoDB
from models.obra import ObraDB


def buscar_obras(session: Session) -> Sequence[ObraDB]:
    return session.exec(select(ObraDB)).all()


def buscar_obra_por_id(obra_id: int, session: Session) -> ObraDB | None:
    return session.get(ObraDB, obra_id)


def adicionar_obra(obra: ObraDB, session: Session) -> ObraDB:
    session.add(obra)
    session.commit()
    session.refresh(obra)
    return obra


def atualizar_obra_bd(obra_id: int, obra: ObraDB, session: Session) -> ObraDB | None:
    obra_existente = session.get(ObraDB, obra_id)
    if not obra_existente:
        return None
    obra_existente.titulo = obra.titulo
    obra_existente.autor = obra.autor
    obra_existente.ano_producao = obra.ano_producao
    session.commit()
    session.refresh(obra_existente)
    return obra_existente


def remover_obra(obra_id: int, session: Session) -> ObraDB | None:
    obra_existente = buscar_obra_por_id(obra_id, session)
    if not obra_existente:
        return None
    session.delete(obra_existente)
    session.commit()
    return obra_existente


def buscar_obras_por_evento(evento_id: int, session: Session) -> Sequence[ObraDB]:
    evento_existente = session.get(EventoDB, evento_id)
    if not evento_existente:
        return []

    return evento_existente.obras
