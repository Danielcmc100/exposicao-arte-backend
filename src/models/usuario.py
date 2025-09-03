from enum import Enum, auto
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship
from .link_rede import LinkRedeDB
from typing import List, Optional

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

    links: List["LinkRedeDB"] = Relationship(back_populates="usuario")
