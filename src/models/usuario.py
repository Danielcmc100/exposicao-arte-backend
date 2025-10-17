from enum import Enum, auto
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from models.avaliacoes_eventos import AvaliacaoEventoDB

if TYPE_CHECKING:
    from models import ComentarioEventoDB, ComentarioObraDB, LinkRedeDB, ObraDB


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

    comentarios_evento: list["ComentarioEventoDB"] = Relationship()

    links: list["LinkRedeDB"] = Relationship()
    obras: list["ObraDB"] = Relationship(back_populates="usuario")  # TODO
    comentarios_obra: list["ComentarioObraDB"] = Relationship(back_populates="usuario")
    avaliacoes_eventos: list["AvaliacaoEventoDB"] = Relationship(back_populates="usuario")
