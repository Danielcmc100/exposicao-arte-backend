"""Modelos de dados para comentários em obras."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .obra import ObraDB
    from .usuario import UsuarioDB


class ComentarioObraBase(SQLModel):
    texto: str
    ativado: bool = True

    usuario_id: int = Field(foreign_key="usuarios.id", nullable=False)
    obra_id: int = Field(foreign_key="obras.id", nullable=False)


class ComentarioObraCreate(ComentarioObraBase): ...


class ComentarioObraResponse(ComentarioObraBase):
    id: int = Field(default=None, primary_key=True)


class ComentarioObraDB(ComentarioObraResponse, table=True):
    __tablename__ = "comentario_obras"  # type: ignore

    usuario: "UsuarioDB" = Relationship()
    obra: "ObraDB" = Relationship()
