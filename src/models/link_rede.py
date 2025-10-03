from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models import UsuarioDB


class LinkRedeBase(SQLModel):
    link: str
    nome_rede: str
    nome_usuario: str
    id_usuario: int = Field(foreign_key="usuarios.id")


class LinkRedeCreate(LinkRedeBase): ...


class LinkRedeResponse(LinkRedeBase):
    id: int


class LinkRedeDB(LinkRedeCreate, table=True):
    __tablename__ = "link_redes"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)

    usuario: "UsuarioDB" = Relationship(back_populates="links")
