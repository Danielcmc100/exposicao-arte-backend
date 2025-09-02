from sqlmodel import Field, SQLModel, Relationship
from enum import Enum, auto
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .usuario import UsuarioDB
    from .evento import EventoDB


class StatusComentario(Enum):
    ATIVO = auto()
    INATIVO = auto()
    PENDENTE = auto()


class ComentarioEventoBase(SQLModel):
    usuario_id: int = Field(foreign_key="usuarios.id")
    evento_id: int = Field(foreign_key="Eventos.id")
    comentario: str
    status: StatusComentario = StatusComentario.ATIVO


class ComentarioEventoCreate(ComentarioEventoBase):
    pass


class ComentarioEventoResponse(ComentarioEventoBase):
    id: int


class ComentarioEventoDB(ComentarioEventoBase, table=True):
    __tablename__ = "comentario_eventos"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)

    usuario: "UsuarioDB" = Relationship(back_populates="comentarios")
    evento: "EventoDB" = Relationship(back_populates="comentarios")
