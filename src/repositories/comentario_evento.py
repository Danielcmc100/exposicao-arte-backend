"""Repositório para operações de comentários em eventos."""

from collections.abc import Sequence

from sqlmodel import Session, select

from models.comentario_evento import ComentarioEventoDB


def buscar_comentarios(session: Session) -> Sequence[ComentarioEventoDB]:
    """Retorna todos os comentários.

    Returns:
        Sequence[ComentarioEventoDB]: Lista de todos os comentários.

    """
    return session.exec(select(ComentarioEventoDB)).all()


def buscar_comentario_por_id(
    comentario_id: int, session: Session
) -> ComentarioEventoDB | None:
    """Busca um comentário pelo ID.

    Returns:
        ComentarioEventoDB | None: Comentário encontrado ou None.

    """
    return session.get(ComentarioEventoDB, comentario_id)


def buscar_comentarios_por_evento(
    evento_id: int, session: Session
) -> Sequence[ComentarioEventoDB]:
    """Retorna todos os comentários de um evento específico.

    Returns:
        Sequence[ComentarioEventoDB]: Lista de comentários do evento.

    """
    return session.exec(
        select(ComentarioEventoDB).where(
            ComentarioEventoDB.evento_id == evento_id
        )
    ).all()


def buscar_comentarios_por_usuario(
    usuario_id: int, session: Session
) -> Sequence[ComentarioEventoDB]:
    """Retorna todos os comentários feitos por um usuário específico.

    Returns:
        Sequence[ComentarioEventoDB]: Lista de comentários do usuário.

    """
    return session.exec(
        select(ComentarioEventoDB).where(
            ComentarioEventoDB.usuario_id == usuario_id
        )
    ).all()


def adicionar_comentario(
    comentario: ComentarioEventoDB, session: Session
) -> ComentarioEventoDB:
    """Adiciona um novo comentário.

    Returns:
        ComentarioEventoDB: Comentário criado.

    """
    session.add(comentario)
    session.commit()
    session.refresh(comentario)
    return comentario


def atualizar_comentario(
    comentario_id: int, comentario: ComentarioEventoDB, session: Session
) -> ComentarioEventoDB | None:
    """Atualiza os dados de um comentário existente.

    Returns
    -------
        ComentarioEventoDB | None: Comentário atualizado ou None se não
            existir.

    """
    comentario_existente = session.get(ComentarioEventoDB, comentario_id)
    if not comentario_existente:
        return None

    comentario_existente.comentario = comentario.comentario
    comentario_existente.status = comentario.status
    session.commit()
    session.refresh(comentario_existente)
    return comentario_existente


def remover_comentario(
    comentario_id: int, session: Session
) -> ComentarioEventoDB | None:
    """Remove um comentário.

    Returns
    -------
        ComentarioEventoDB | None: Comentário removido ou None se não existir.

    """
    comentario_existente = buscar_comentario_por_id(comentario_id, session)
    if not comentario_existente:
        return None
    session.delete(comentario_existente)
    session.commit()
    return comentario_existente
