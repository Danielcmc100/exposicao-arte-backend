from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    pass


class CategoriaBase(SQLModel):
    nome: str


class CategoriaCreate(CategoriaBase):
    nome: str


class CategoriaResponse(CategoriaBase):
    id: int


class CategoriaDB(CategoriaCreate, table=True):
    __tablename__ = "categorias"  # type: ignore

    id: int = Field(default=None, primary_key=True)
    # obras: list["ObraDB"] = Relationship() # TODO
