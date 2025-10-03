from typing import Sequence

from sqlmodel import Session, select

from models.comentario_obra import ComentarioObraDB


def buscar_comentarios_obras(session: Session) -> Sequence[ComentarioObraDB]:
    return session.exec(select(ComentarioObraDB)).all()


def buscar_comentario_obra_por_id(
    comentario_id: int, session: Session
) -> ComentarioObraDB | None:
    return session.get(ComentarioObraDB, comentario_id)


def adicionar_comentario_obra(
    comentario: ComentarioObraDB, session: Session
) -> ComentarioObraDB:
    session.add(comentario)
    session.commit()
    session.refresh(comentario)
    return comentario


def atualizar_comentario_obra_bd(
    comentario_obra_id: int, comentario: ComentarioObraDB, session: Session
) -> ComentarioObraDB | None:
    comentario_obra_existente = session.get(ComentarioObraDB, comentario_obra_id)
    if not comentario_obra_existente:
        return None

    for fiend, value in comentario.model_dump().values():
        setattr(comentario_obra_existente, fiend, value)

    session.commit()
    session.refresh(comentario_obra_existente)
    return comentario_obra_existente


def remover_comentario_obra(
    comentario_obra_id: int, session: Session
) -> ComentarioObraDB | None:
    comentario_obra_existente = buscar_comentario_obra_por_id(
        comentario_obra_id, session
    )
    if not comentario_obra_existente:
        return None
    session.delete(comentario_obra_existente)
    session.commit()
    return comentario_obra_existente
