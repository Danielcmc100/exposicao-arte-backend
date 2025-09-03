from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

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
    __tablename__ = "Eventos"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)

    comentarios: List["ComentarioEventoDB"] = Relationship(back_populates="evento")
