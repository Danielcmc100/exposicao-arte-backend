from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class LinkRedeBase(SQLModel):
    link: str
    nome_rede: str
    nome_usuario: str
    id_usuario: int = Field(foreign_key="usuarios.id")


class LinkRedeCreate(LinkRedeBase):
    pass


class LinkRedeResponse(LinkRedeBase):
    id: int


class LinkRedeDB(LinkRedeCreate, table=True):
    __tablename__ = "link_redes"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)

    usuario: Optional["UsuarioDB"] = Relationship(back_populates="links")