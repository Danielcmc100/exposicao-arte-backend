from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .obra import ObraDB
    from .usuario import UsuarioDB


class ComentarioObraBase(SQLModel):
    ativado: bool = True


class ComentarioObraCreate(ComentarioObraBase): ...


class ComentarioObraResponse(ComentarioObraBase):
    id: int


class ComentarioObraDB(ComentarioObraCreate, table=True):
    __tablename__ = "comentario_obras"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)

    usuario_id: int = Field(foreign_key="usuarios.id", nullable=False)
    usuario: "UsuarioDB" = Relationship()

    obra_id: int = Field(foreign_key="obras.id", nullable=False)
    obra: "ObraDB" = Relationship()
