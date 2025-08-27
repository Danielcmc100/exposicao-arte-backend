from datetime import datetime

from sqlalchemy import JSON
from sqlmodel import Field, SQLModel, func


class ObraBase(SQLModel):
    titulo: str
    autor: str
    ano_producao: datetime
    tecnica_criacao: str
    altura_centimetros: float
    largura_centimetros: float
    peso_quilos: float
    tags: list[str] = Field(sa_type=JSON)
    preco: float
    preco: float
    status: bool


class ObraDB(ObraBase, table=True):
    __tablename__ = "obras"  # type: ignore
    id: int = Field(default=None, primary_key=True)
    data_postagem: datetime = Field(default=func.now())
    id_artista: int
    id_categoria: int
