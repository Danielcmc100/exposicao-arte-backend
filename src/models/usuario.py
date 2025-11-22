"""Modelos de dados para usuários do sistema."""

from enum import Enum, auto
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models import (
        AvaliacaoEventoDB,
        ComentarioEventoDB,
        ComentarioObraDB,
        LinkRedeDB,
        ObraDB,
    )


class Funcao(Enum):
    CONSUMIDOR = auto()
    ARTISTA = auto()
    ADMIN = auto()


class UsuarioBase(SQLModel):
    """Campos básicos de um usuário (usado como base para outros modelos)."""

    nome: str
    email: EmailStr
    funcao: Funcao
    biografia: str


class UsuarioCreate(UsuarioBase):
    """Modelo usado na criação de usuário (input da API)."""

    senha: str


class UsuarioLogin(SQLModel):
    """Modelo usado no endpoint de login."""

    email: EmailStr
    senha: str


class UsuarioResponse(UsuarioBase):
    """Modelo retornado nas respostas da API (output)."""

    id: int


class UsuarioDB(SQLModel, table=True):
    """Modelo persistido no banco de dados."""

    __tablename__ = "usuarios"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: EmailStr = Field(index=True, unique=True, nullable=False)
    funcao: Funcao
    biografia: str
    senha_hash: str

    comentarios_evento: list["ComentarioEventoDB"] = Relationship()
    links: list["LinkRedeDB"] = Relationship()
    obras: list["ObraDB"] = Relationship(back_populates="usuario")
    comentarios_obra: list["ComentarioObraDB"] = Relationship(
        back_populates="usuario"
    )
    avaliacoes_eventos: list["AvaliacaoEventoDB"] = Relationship(
        back_populates="usuario"
    )
