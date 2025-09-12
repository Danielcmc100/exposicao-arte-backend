from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .comentario_evento import ComentarioEventoDB


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

    id: int | None = Field(default=None, primary_key=True)

    comentarios: List["ComentarioEventoDB"] = Relationship(back_populates="evento")
