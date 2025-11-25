"""Modelos de dados para avaliacao_obra."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .obra import ObraDB
    from .usuario import UsuarioDB


class AvaliacaoObraCreate(SQLModel):
    id_obra: int = Field(foreign_key="obras.id")
    id_usuario: int = Field(foreign_key="usuarios.id")
    gostou: bool
    avaliacao: int = Field(gt=0, lt=11)


class AvaliacaoObraResponse(AvaliacaoObraCreate):
    id: int = Field(default=None, primary_key=True)


class AvaliacaoObraDB(AvaliacaoObraResponse, table=True):
    __tablename__ = "avaliacoes_obras"  # type: ignore

    usuario: "UsuarioDB" = Relationship()
    obra: "ObraDB" = Relationship()
