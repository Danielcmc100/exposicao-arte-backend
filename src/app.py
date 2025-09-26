from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db
from routers.categoria import rota as categoria_rota
from routers.evento import rota as evento_rota
from routers.link_rede import rota as link_rede_rota
from routers.usuario import rota as usuario_rota
from routers.obra import rota as obra_rota


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


app.include_router(usuario_rota)
app.include_router(link_rede_rota)
app.include_router(categoria_rota)
app.include_router(evento_rota)
app.include_router(obra_rota)
