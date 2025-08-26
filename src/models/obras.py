from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy.sql import func

class ObraBase(SQLModel):
    titulo: str
    autor: str
    ano_producao: datetime  
    tecnica_criacao: str
    altura_centimetros: float
    largura_centimetros: float
    comprimento_centimetros: float
    peso_quilos: float
    tags: list[str]
    preco: float
    status: bool

class ObraDB(ObraBase, table=True):
    __tablename__ = "obras" # type: ignore
    id: int = Field(default=None, primary_key=True)
    data_postagem: datetime = Field (default = func.now())
    id_artista: int
    id_categoria: int
   

    










    