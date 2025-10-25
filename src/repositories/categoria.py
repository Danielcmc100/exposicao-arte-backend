"""Repositório para operações de categorias."""

from collections.abc import Sequence

from sqlmodel import Session, select

from models.categoria import CategoriaDB


def buscar_categorias(session: Session) -> Sequence[CategoriaDB]:
    """Retorna todas as categorias.

    Args:
        session: Sessão do banco de dados.

    Returns:
        Sequence[CategoriaDB]: Lista de categorias.

    """
    return session.exec(select(CategoriaDB)).all()


def buscar_categoria_por_id(
    categoria_id: int, session: Session
) -> CategoriaDB | None:
    """Busca uma categoria pelo ID.

    Args:
        categoria_id: ID da categoria.
        session: Sessão do banco de dados.

    Returns:
        CategoriaDB | None: Categoria encontrada ou None.

    """
    return session.get(CategoriaDB, categoria_id)


def adicionar_categoria(
    categoria: CategoriaDB, session: Session
) -> CategoriaDB:
    """Adiciona uma nova categoria.

    Args:
        categoria: Dados da categoria a ser adicionada.
        session: Sessão do banco de dados.

    Returns:
        CategoriaDB: Categoria adicionada.

    """
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


def atualizar_categoria_bd(
    categoria_id: int, categoria: CategoriaDB, session: Session
) -> CategoriaDB | None:
    """Atualiza uma categoria existente.

    Args:
        categoria_id: ID da categoria a ser atualizada.
        categoria: Novos dados da categoria.
        session: Sessão do banco de dados.

    Returns:
        CategoriaDB | None: Categoria atualizada ou None.

    """
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
    """Remove uma categoria.

    Args:
        categoria_id: ID da categoria a ser removida.
        session: Sessão do banco de dados.

    Returns:
        CategoriaDB | None: Categoria removida ou None.

    """
    categoria_existente = buscar_categoria_por_id(categoria_id, session)
    if not categoria_existente:
        return None
    session.delete(categoria_existente)
    session.commit()
    return categoria_existente
