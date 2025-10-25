from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .evento import EventoDB
    from .usuario import UsuarioDB

class AvaliacaoEventoBase(SQLModel):
    usuario_id: int = Field(foreign_key="usuarios.id")
    evento_id: int = Field(foreign_key="eventos.id")
    gostou: str
    avaliacao: int

class AvaliacaoEventoCreate(AvaliacaoEventoBase): ...


class AvaliacaoEventoResponse(AvaliacaoEventoBase):
    id: int = Field(default=None, primary_key=True)


class AvaliacaoEventoDB(AvaliacaoEventoResponse, table=True):
    __tablename__ = "avaliacoes_eventos"  # type: ignore

    usuario: "UsuarioDB" = Relationship()
    evento: "EventoDB" = Relationship()
