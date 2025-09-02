from typing import Sequence

from sqlmodel import Session, select

from models.comentario_evento import ComentarioEventoDB


def buscar_comentarios(session: Session) -> Sequence[ComentarioEventoDB]:
    """Retorna todos os comentários."""
    return session.exec(select(ComentarioEventoDB)).all()


def buscar_comentario_por_id(comentario_id: int, session: Session) -> ComentarioEventoDB | None:
    """Busca um comentário pelo ID."""
    return session.get(ComentarioEventoDB, comentario_id)


def buscar_comentarios_por_evento(evento_id: int, session: Session) -> Sequence[ComentarioEventoDB]:
    """Retorna todos os comentários de um evento específico."""
    return session.exec(
        select(ComentarioEventoDB).where(ComentarioEventoDB.evento_id == evento_id)
    ).all()


def buscar_comentarios_por_usuario(usuario_id: int, session: Session) -> Sequence[ComentarioEventoDB]:
    """Retorna todos os comentários feitos por um usuário específico."""
    return session.exec(
        select(ComentarioEventoDB).where(ComentarioEventoDB.usuario_id == usuario_id)
    ).all()


def adicionar_comentario(comentario: ComentarioEventoDB, session: Session) -> ComentarioEventoDB:
    """Adiciona um novo comentário."""
    session.add(comentario)
    session.commit()
    session.refresh(comentario)
    return comentario


def atualizar_comentario(
    comentario_id: int, comentario: ComentarioEventoDB, session: Session
) -> ComentarioEventoDB | None:
    """Atualiza os dados de um comentário existente."""
    comentario_existente = session.get(ComentarioEventoDB, comentario_id)
    if not comentario_existente:
        return None

    comentario_existente.comentario = comentario.comentario
    comentario_existente.status = comentario.status
    session.commit()
    session.refresh(comentario_existente)
    return comentario_existente


def remover_comentario(comentario_id: int, session: Session) -> ComentarioEventoDB | None:
    """Remove um comentário."""
    comentario_existente = buscar_comentario_por_id(comentario_id, session)
    if not comentario_existente:
        return None
    session.delete(comentario_existente)
    session.commit()
    return comentario_existente
