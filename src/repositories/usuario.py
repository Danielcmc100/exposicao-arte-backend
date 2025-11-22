"""Repositório para operações de usuários."""

from collections.abc import Sequence

from sqlmodel import Session, select

from models.usuario import UsuarioDB


def get_usuario_by_email(session: Session, email: str) -> UsuarioDB | None:
    """Busca um usuário pelo e-mail.

    Args:
        session: Sessão do banco de dados.
        email: E-mail do usuário.

    Returns:
        UsuarioDB | None: O usuário encontrado ou None.

    """
    stmt = select(UsuarioDB).where(UsuarioDB.email == email)
    return session.exec(stmt).first()


def buscar_usuarios(session: Session) -> Sequence[UsuarioDB]:
    """Retorna todos os usuários.

    Args:
        session: Sessão do banco de dados.

    Returns:
        Sequence[UsuarioDB]: Lista de usuários.

    """
    return session.exec(select(UsuarioDB)).all()


def buscar_usuario_por_id(
    usuario_id: int, session: Session
) -> UsuarioDB | None:
    """Busca um usuário pelo ID.

    Args:
        usuario_id: ID do usuário.
        session: Sessão do banco de dados.

    Returns:
        UsuarioDB | None: Usuário encontrado ou None.

    """
    return session.get(UsuarioDB, usuario_id)


def adicionar_usuario(usuario: UsuarioDB, session: Session) -> UsuarioDB:
    """Adiciona um novo usuário.

    Args:
        usuario: Dados do usuário a ser adicionado.
        session: Sessão do banco de dados.

    Returns:
        UsuarioDB: Usuário adicionado.

    """
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


def atualizar_usuario_bd(
    usuario_id: int, usuario: UsuarioDB, session: Session
) -> UsuarioDB | None:
    """Atualiza um usuário existente.

    Args:
        usuario_id: ID do usuário a ser atualizado.
        usuario: Novos dados do usuário.
        session: Sessão do banco de dados.

    Returns:
        UsuarioDB | None: Usuário atualizado ou None.

    """
    usuario_existente = session.get(UsuarioDB, usuario_id)
    if not usuario_existente:
        return None
    usuario_existente.nome = usuario.nome
    usuario_existente.email = usuario.email
    session.commit()
    session.refresh(usuario_existente)
    return usuario_existente


def remover_usuario(usuario_id: int, session: Session) -> UsuarioDB | None:
    """Remove um usuário.

    Args:
        usuario_id: ID do usuário a ser removido.
        session: Sessão do banco de dados.

    Returns:
        UsuarioDB | None: Usuário removido ou None.

    """
    usuario_existente = buscar_usuario_por_id(usuario_id, session)
    if not usuario_existente:
        return None
    session.delete(usuario_existente)
    session.commit()
    return usuario_existente
