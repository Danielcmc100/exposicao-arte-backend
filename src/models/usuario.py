from enum import Enum, auto
from typing import TYPE_CHECKING, List

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .comentario_evento import ComentarioEventoDB
    from .link_rede import LinkRedeDB


class Funcao(Enum):
    CONSUMIDOR = auto()
    ARTISTA = auto()
    ADMIN = auto()


class UsuarioBase(SQLModel):
    nome: str
    email: EmailStr
    funcao: Funcao
    biografia: str


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioResponse(UsuarioBase):
    id: int


class UsuarioDB(UsuarioCreate, table=True):
    __tablename__ = "usuarios"  # type: ignore

    id: int = Field(default=None, primary_key=True)

    comentarios: List["ComentarioEventoDB"] = Relationship(back_populates="usuario")

    links: List["LinkRedeDB"] = Relationship(back_populates="usuario")
