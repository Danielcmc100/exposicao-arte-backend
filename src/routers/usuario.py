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
    return buscar_usuarios(session)


@rota.get("/{usuario_id}")
def ler_usuario(usuario_id: int, session: SessionInjetada) -> UsuarioResponse | None:
    return buscar_usuario_por_id(usuario_id, session)


@rota.post("/")
def criar_usuario(usuario: UsuarioCreate, session: SessionInjetada) -> UsuarioResponse:
    usuario_db_instance = UsuarioDB(usuario.__dict__)
    return adicionar_usuario(usuario_db_instance, session)


@rota.put("/{usuario_id}")
def atualizar_usuario(
    usuario_id: int, usuario: UsuarioCreate, session: SessionInjetada
) -> UsuarioResponse | None:
    return atualizar_usuario_bd(usuario_id, usuario, session)


@rota.delete("/{usuario_id}")
def excluir_usuario(
    usuario_id: int, session: SessionInjetada
) -> UsuarioResponse | None:
    return remover_usuario(usuario_id, session)
