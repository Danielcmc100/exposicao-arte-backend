from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UsuarioBase(SQLModel):
    nome: str
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioResponse(UsuarioBase):
    id: int


class UsuarioDB(UsuarioCreate, table=True):
    id: int = Field(default=None, primary_key=True)
