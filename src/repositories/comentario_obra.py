"""Repositório para operações de comentários de obras."""

from collections.abc import Sequence

from sqlmodel import Session, select

from models.comentario_obra import ComentarioObraDB


def buscar_comentarios_obras(session: Session) -> Sequence[ComentarioObraDB]:
    """Retorna todos os comentários de obras.

    Args:
        session: Sessão do banco de dados.

    Returns:
        Sequence[ComentarioObraDB]: Lista de comentários de obras.

    """
    return session.exec(select(ComentarioObraDB)).all()


def buscar_comentario_obra_por_id(
    comentario_id: int, session: Session
) -> ComentarioObraDB | None:
    """Busca um comentário de obra pelo ID.

    Args:
        comentario_id: ID do comentário.
        session: Sessão do banco de dados.

    Returns:
        ComentarioObraDB | None: Comentário encontrado ou None.

    """
    return session.get(ComentarioObraDB, comentario_id)


def adicionar_comentario_obra(
    comentario: ComentarioObraDB, session: Session
) -> ComentarioObraDB:
    """Adiciona um novo comentário de obra.

    Args:
        comentario: Dados do comentário a ser adicionado.
        session: Sessão do banco de dados.

    Returns:
        ComentarioObraDB: Comentário adicionado.

    """
    session.add(comentario)
    session.commit()
    session.refresh(comentario)
    return comentario


def atualizar_comentario_obra_bd(
    comentario_obra_id: int, comentario: ComentarioObraDB, session: Session
) -> ComentarioObraDB | None:
    """Atualiza um comentário de obra existente.

    Args:
        comentario_obra_id: ID do comentário a ser atualizado.
        comentario: Novos dados do comentário.
        session: Sessão do banco de dados.

    Returns:
        ComentarioObraDB | None: Comentário atualizado ou None.

    """
    comentario_obra_existente = session.get(
        ComentarioObraDB, comentario_obra_id
    )
    if not comentario_obra_existente:
        return None

    for field, value in comentario.model_dump().items():
        setattr(comentario_obra_existente, field, value)

    session.commit()
    session.refresh(comentario_obra_existente)
    return comentario_obra_existente


def remover_comentario_obra(
    comentario_obra_id: int, session: Session
) -> ComentarioObraDB | None:
    """Remove um comentário de obra.

    Args:
        comentario_obra_id: ID do comentário a ser removido.
        session: Sessão do banco de dados.

    Returns:
        ComentarioObraDB | None: Comentário removido ou None.

    """
    comentario_obra_existente = buscar_comentario_obra_por_id(
        comentario_obra_id, session
    )
    if not comentario_obra_existente:
        return None
    session.delete(comentario_obra_existente)
    session.commit()
    return comentario_obra_existente
