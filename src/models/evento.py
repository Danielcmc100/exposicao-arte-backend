from sqlmodel import Field, SQLModel
from datetime import datetime

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