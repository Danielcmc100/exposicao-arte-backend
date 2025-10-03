from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel, func

if TYPE_CHECKING:
    from .categoria import CategoriaDB
    from .comentario_obra import ComentarioObraDB
    from .usuario import UsuarioDB


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

    usuario_id: int = Field(foreign_key="usuarios.id", nullable=False)
    categoria_id: int = Field(foreign_key="categorias.id", nullable=False)


class ObraCreate(ObraBase): ...


class ObraResponse(ObraBase):
    id: int = Field(default=None, primary_key=True)


class ObraDB(ObraResponse, table=True):
    __tablename__ = "obras"  # type: ignore

    usuario: "UsuarioDB" = Relationship(
        back_populates="obras",
        sa_relationship_kwargs={"foreign_keys": ("ObraDB.usuario_id")},
    )

    categoria: "CategoriaDB" = Relationship(
        back_populates="obras",
        sa_relationship_kwargs={"foreign_keys": ("ObraDB.categoria_id")},
    )

    comentarios_obra: list["ComentarioObraDB"] = Relationship(back_populates="obra")
