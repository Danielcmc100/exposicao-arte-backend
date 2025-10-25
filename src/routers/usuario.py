"""Rotas para gerenciamento de usuários."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from models.usuario import UsuarioCreate, UsuarioDB, UsuarioResponse
from repositories.usuario import (
    adicionar_usuario,
    atualizar_usuario_bd,
    buscar_usuario_por_id,
    buscar_usuarios,
    remover_usuario,
)

rota = APIRouter(prefix="/usuarios", tags=["usuarios"])


SessionInjetada = Annotated[Session, Depends(get_session)]


@rota.get("/")
def obter_usuarios(session: SessionInjetada) -> list[UsuarioResponse]:
    """Recupera todos os usuários do banco de dados.

    Returns:
        list[UsuarioResponse]: Lista de usuários.

    """
    usuarios_list = buscar_usuarios(session)
    return list(map(UsuarioResponse.model_validate, usuarios_list))


@rota.get("/{usuario_id}")
def ler_usuario(
    usuario_id: int, session: SessionInjetada
) -> UsuarioResponse | None:
    """Recupera um usuário específico pelo seu ID.

    Returns:
        UsuarioResponse | None: Usuário encontrado ou None se não existir.

    """
    usuario = buscar_usuario_por_id(usuario_id, session)
    return UsuarioResponse.model_validate(usuario) if usuario else None


@rota.post("/")
def criar_usuario(
    usuario: UsuarioCreate, session: SessionInjetada
) -> UsuarioResponse:
    """Cria um novo usuário no banco de dados.

    Returns:
        UsuarioResponse: Dados do usuário criado.

    """
    usuario_db = UsuarioDB.model_validate(usuario)
    return UsuarioResponse.model_validate(
        adicionar_usuario(usuario_db, session)
    )


@rota.put("/{usuario_id}")
def atualizar_usuario(
    usuario_id: int, usuario: UsuarioCreate, session: SessionInjetada
) -> UsuarioResponse | None:
    """Atualiza os dados de um usuário existente.

    Returns:
        UsuarioResponse | None: Usuário atualizado ou None se não existir.

    """
    usuario_db = UsuarioDB.model_validate(usuario)
    usuario_atualizado = atualizar_usuario_bd(usuario_id, usuario_db, session)
    return UsuarioResponse.model_validate(usuario_atualizado)


@rota.delete("/{usuario_id}")
def excluir_usuario(
    usuario_id: int, session: SessionInjetada
) -> UsuarioResponse | None:
    """Remove um usuário do banco de dados.

    Returns:
        UsuarioResponse | None: Usuário removido ou None se não existir.

    """
    usuario_removido = remover_usuario(usuario_id, session)
    return UsuarioResponse.model_validate(usuario_removido)
