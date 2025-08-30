from sqlmodel import Field, SQLModel

class LinkRedeBase(SQLModel):
    link: str
    nome_rede: str
    nome_usuario: str
    id_usuario: int = Field(foreign_key="usuarios.id")


class LinkRedeCreate(LinkRedeBase):
    nome: str


class LinkRedeResponse(LinkRedeBase):
    id: int


class LinkRedeDB(LinkRedeCreate, table=True):
    __tablename__ = "LinkRedes"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)