from typing import TYPE_CHECKING, Optional

from datetime import datetime

from sqlalchemy import JSON
from sqlmodel import Field, SQLModel, func, Relationship

if TYPE_CHECKING:
    from .usuario import UsuarioDB
    from .categoria import CategoriaDB


class ObraBase(SQLModel):
    titulo: str
    autor: str
    ano_producao: int
    tecnica_criacao: str
    altura_centimetros: float
    largura_centimetros: float
    peso_quilos: float
    tags: list[str] = Field(sa_type=JSON)
    preco: float
    status: bool
    data_postagem: datetime = Field(default=func.now())
    id_artista: int
    id_categoria: int

class ObraCreate(ObraBase):
    pass


class ObraResponse(ObraBase):
    id: int

class ObraDB(ObraCreate, table=True):
    __tablename__ = "obras"  # type: ignore
    id: int = Field(default=None, primary_key=True)

    usuario_id: int = Field(foreign_key="usuarios.id", nullable=False)
    usuario: "UsuarioDB" = Relationship(back_populates="obras")

    categoria_id: int = Field(foreign_key="categorias.id", nullable=False)
    categoria: "CategoriaDB" = Relationship(back_populates="obras")