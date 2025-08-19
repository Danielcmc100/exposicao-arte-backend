
from pydantic import BaseModel
from fastapi import APIRouter


class Cachorro(BaseModel):
    id: int
    nome: str
    idade: int
    raca: str

rota = APIRouter()

@rota.post("/cachorros")
def listar_cachorros(cachorro: Cachorro):
    return {"cachorros": [cachorro]}

