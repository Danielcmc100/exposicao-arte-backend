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
    usuarios_list = buscar_usuarios(session)
    return list(map(UsuarioResponse.model_validate, usuarios_list))


@rota.get("/{usuario_id}")
def ler_usuario(
    usuario_id: int, session: SessionInjetada
) -> UsuarioResponse | None:
    usuario = buscar_usuario_por_id(usuario_id, session)
    return UsuarioResponse.model_validate(usuario) if usuario else None


@rota.post("/")
def criar_usuario(
    usuario: UsuarioCreate, session: SessionInjetada
) -> UsuarioResponse:
    usuario_db = UsuarioDB.model_validate(usuario)
    return UsuarioResponse.model_validate(
        adicionar_usuario(usuario_db, session)
    )


@rota.put("/{usuario_id}")
def atualizar_usuario(
    usuario_id: int, usuario: UsuarioCreate, session: SessionInjetada
) -> UsuarioResponse | None:
    usuario_db = UsuarioDB.model_validate(usuario)
    usuario_atualizado = atualizar_usuario_bd(usuario_id, usuario_db, session)
    return UsuarioResponse.model_validate(usuario_atualizado)


@rota.delete("/{usuario_id}")
def excluir_usuario(
    usuario_id: int, session: SessionInjetada
) -> UsuarioResponse | None:
    usuario_removido = remover_usuario(usuario_id, session)
    return UsuarioResponse.model_validate(usuario_removido)
