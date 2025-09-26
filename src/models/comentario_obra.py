from sqlmodel import Field, SQLModel


class ComentarioObraBase(SQLModel):
    ativado: bool = True
    id_obra: int = Field(foreign_key="usuarios.id")
    id_usuario: int = Field(foreign_key="usuarios.id")


class ComentarioObraCreate(ComentarioObraBase):
    pass


class ComentarioObraResponse(ComentarioObraBase):
    id: int


class ComentarioObraDB(ComentarioObraCreate, table=True):
    __tablename__ = "comentario_obras"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
