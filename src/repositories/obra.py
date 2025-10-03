from typing import Sequence

from sqlmodel import Session, select

from models.obra import ObraDB


def buscar_obras(session: Session) -> Sequence[ObraDB]:
    obras = session.exec(select(ObraDB)).all()
    print([a.eventos for a in obras])
    return obras


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
