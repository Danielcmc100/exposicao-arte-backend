from collections.abc import Sequence

from sqlmodel import Session, select

from models.categoria import CategoriaDB


def buscar_categorias(session: Session) -> Sequence[CategoriaDB]:
    return session.exec(select(CategoriaDB)).all()


def buscar_categoria_por_id(
    categoria_id: int, session: Session
) -> CategoriaDB | None:
    return session.get(CategoriaDB, categoria_id)


def adicionar_categoria(
    categoria: CategoriaDB, session: Session
) -> CategoriaDB:
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


def atualizar_categoria_bd(
    categoria_id: int, categoria: CategoriaDB, session: Session
) -> CategoriaDB | None:
    categoria_existente = session.get(CategoriaDB, categoria_id)
    if not categoria_existente:
        return None
    categoria_existente.nome = categoria.nome
    session.commit()
    session.refresh(categoria_existente)
    return categoria_existente


def remover_categoria(
    categoria_id: int, session: Session
) -> CategoriaDB | None:
    categoria_existente = buscar_categoria_por_id(categoria_id, session)
    if not categoria_existente:
        return None
    session.delete(categoria_existente)
    session.commit()
    return categoria_existente
