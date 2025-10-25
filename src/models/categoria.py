"""Modelos de dados para categorias de obras."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models import ObraDB


class CategoriaBase(SQLModel):
    nome: str


class CategoriaCreate(CategoriaBase):
    nome: str


class CategoriaResponse(CategoriaBase):
    id: int


class CategoriaDB(CategoriaCreate, table=True):
    __tablename__ = "categorias"  # type: ignore

    id: int = Field(default=None, primary_key=True)
    obras: list["ObraDB"] = Relationship()
