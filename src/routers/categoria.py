"""Rotas para gerenciamento de categorias de obras."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from models.categoria import CategoriaCreate, CategoriaDB, CategoriaResponse
from repositories.categoria import (
    adicionar_categoria,
    atualizar_categoria_bd,
    buscar_categoria_por_id,
    buscar_categorias,
    remover_categoria,
)

rota = APIRouter(prefix="/categorias", tags=["categorias"])


SessionInjetada = Annotated[Session, Depends(get_session)]


@rota.get("/")
def obter_categorias(session: SessionInjetada) -> list[CategoriaResponse]:
    """Recupera todas as categorias do banco de dados.

    Returns:
        list[CategoriaResponse]: Lista de categorias.

    """
    categorias_list = buscar_categorias(session)
    return list(map(CategoriaResponse.model_validate, categorias_list))


@rota.get("/{categoria_id}")
def ler_categoria(
    categoria_id: int, session: SessionInjetada
) -> CategoriaResponse | None:
    """Recupera uma categoria específica pelo seu ID.

    Returns:
        CategoriaResponse | None: Categoria encontrada ou None se não existir.

    """
    categoria = buscar_categoria_por_id(categoria_id, session)
    return CategoriaResponse.model_validate(categoria) if categoria else None


@rota.post("/")
def criar_categoria(
    categoria: CategoriaCreate, session: SessionInjetada
) -> CategoriaResponse:
    """Cria uma nova categoria no banco de dados.

    Returns:
        CategoriaResponse: Dados da categoria criada.

    """
    categoria_db = CategoriaDB.model_validate(categoria)
    return CategoriaResponse.model_validate(
        adicionar_categoria(categoria_db, session)
    )


@rota.put("/{categoria_id}")
def atualizar_categoria(
    categoria_id: int, categoria: CategoriaCreate, session: SessionInjetada
) -> CategoriaResponse | None:
    """Atualiza os dados de uma categoria existente.

    Returns:
        CategoriaResponse | None: Categoria atualizada ou None se não existir.

    """
    categoria_db = CategoriaDB.model_validate(categoria)
    categoria_atualizada = atualizar_categoria_bd(
        categoria_id, categoria_db, session
    )
    return CategoriaResponse.model_validate(categoria_atualizada)


@rota.delete("/{categoria_id}")
def excluir_categoria(
    categoria_id: int, session: SessionInjetada
) -> CategoriaResponse | None:
    """Remove uma categoria do banco de dados.

    Returns:
        CategoriaResponse | None: Categoria removida ou None se não existir.

    """
    categoria_removida = remover_categoria(categoria_id, session)
    return CategoriaResponse.model_validate(categoria_removida)
