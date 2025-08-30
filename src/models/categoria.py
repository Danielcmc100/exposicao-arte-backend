from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class CategoriaBase(SQLModel):
    nome: str


class CategoriaCreate(CategoriaBase):
    nome: str


class CategoriaResponse(CategoriaBase):
    id: int


class CategoriaDB(CategoriaCreate, table=True):
    __tablename__ = "Categorias"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
