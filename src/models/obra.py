from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel, func

if TYPE_CHECKING:
    from models import CategoriaDB


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
    preco: float
    status: bool


class ObraDB(ObraBase, table=True):
    __tablename__ = "obra"  # type: ignore
    id: int = Field(default=None, primary_key=True)
    data_postagem: datetime = Field(default=func.now())
    id_artista: int

    id_categoria: int = Field(foreign_key="categorias.id")
    categoria: "CategoriaDB" = Relationship()  # back_populates="obras"
