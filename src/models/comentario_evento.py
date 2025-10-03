from enum import Enum, auto
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models import EventoDB, UsuarioDB


class StatusComentario(Enum):
    ATIVO = auto()
    INATIVO = auto()
    PENDENTE = auto()


class ComentarioEventoBase(SQLModel):
    usuario_id: int = Field(foreign_key="usuarios.id")
    evento_id: int = Field(foreign_key="eventos.id")
    comentario: str
    status: StatusComentario = StatusComentario.ATIVO


class ComentarioEventoCreate(ComentarioEventoBase): ...


class ComentarioEventoResponse(ComentarioEventoBase):
    id: int


class ComentarioEventoDB(ComentarioEventoBase, table=True):
    __tablename__ = "comentario_eventos"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)

    usuario: "UsuarioDB" = Relationship(back_populates="comentarios_evento")
    evento: "EventoDB" = Relationship(back_populates="comentarios")
