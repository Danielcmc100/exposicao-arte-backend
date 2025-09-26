from typing import TYPE_CHECKING, List
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .obra import ObraDB

class CategoriaBase(SQLModel):
    nome: str


class CategoriaCreate(CategoriaBase):
    nome: str


class CategoriaResponse(CategoriaBase):
    id: int


class CategoriaDB(CategoriaCreate, table=True):
    __tablename__ = "categorias"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)

    obras: List["ObraDB"] = Relationship(back_populates="usuario")
