from typing import Sequence

from sqlmodel import Session, select

from models.usuario import UsuarioDB


def buscar_usuarios(session: Session) -> Sequence[UsuarioDB]:
    return session.exec(select(UsuarioDB)).all()


def buscar_usuario_por_id(usuario_id: int, session: Session) -> UsuarioDB | None:
    return session.get(UsuarioDB, usuario_id)


def adicionar_usuario(usuario: UsuarioDB, session: Session) -> UsuarioDB:
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


def atualizar_usuario_bd(
    usuario_id: int, usuario: UsuarioDB, session: Session
) -> UsuarioDB | None:
    usuario_existente = session.get(UsuarioDB, usuario_id)
    if not usuario_existente:
        return None
    usuario_existente.nome = usuario.nome
    usuario_existente.email = usuario.email
    session.commit()
    session.refresh(usuario_existente)
    return usuario_existente


def remover_usuario(usuario_id: int, session: Session) -> UsuarioDB | None:
    usuario_existente = buscar_usuario_por_id(usuario_id, session)
    if not usuario_existente:
        return None
    session.delete(usuario_existente)
    session.commit()
    return usuario_existente
