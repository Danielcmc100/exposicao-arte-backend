"""Rotas para gerenciamento de usuários."""

from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from database import get_session
from models.usuario import UsuarioCreate, UsuarioDB, UsuarioResponse
from security import get_password_hash
from repositories.usuario import (
    adicionar_usuario,
    atualizar_usuario_bd,
    buscar_usuario_por_id,
    buscar_usuarios,
    remover_usuario,
    get_usuario_by_email
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


@rota.post("/", status_code=status.HTTP_201_CREATED)
def criar_usuario(
    usuario: UsuarioCreate, session: SessionInjetada
) -> UsuarioResponse:
    """Cria um novo usuário no banco de dados.

    Returns:
        UsuarioResponse: Usuário criado.

    """
    usuario_existente = get_usuario_by_email(session, usuario.email)
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário com este email já existe.",
        )

    usuario_db = UsuarioDB(
        nome=usuario.nome,
        email=usuario.email,
        funcao=usuario.funcao,
        biografia=usuario.biografia,
        senha_hash=get_password_hash(usuario.senha),
    ) # type: ignore
    novo_usuario = adicionar_usuario(usuario_db, session)
    return UsuarioResponse.model_validate(novo_usuario)

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
