"""Modelos de dados para eventos culturais."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .obra_evento import ObraEventoDB

if TYPE_CHECKING:
    from models import ComentarioEventoDB, ObraDB, UsuarioDB

    from .avaliacoes_eventos import AvaliacaoEventoDB


class EventoBase(SQLModel):
    endereco: str
    local: str
    data: datetime
    id_organizador: int = Field(foreign_key="usuarios.id")
    id_responsavel: int = Field(foreign_key="usuarios.id")


class EventoCreate(EventoBase):
    nome: str


class EventoResponse(EventoBase):
    id: int


class EventoDB(EventoCreate, table=True):
    __tablename__ = "eventos"  # type: ignore

    id: int = Field(default=None, primary_key=True)

    organizador: "UsuarioDB" = Relationship(
        sa_relationship_kwargs={"foreign_keys": ("EventoDB.id_organizador")}
    )
    responsavel: "UsuarioDB" = Relationship(
        sa_relationship_kwargs={"foreign_keys": ("EventoDB.id_responsavel")}
    )
    comentarios: list["ComentarioEventoDB"] = Relationship()
    obras: list["ObraDB"] = Relationship(
        back_populates="eventos", link_model=ObraEventoDB
    )
    avaliacoes_eventos: list["AvaliacaoEventoDB"] = Relationship(
        back_populates="evento"
    )
