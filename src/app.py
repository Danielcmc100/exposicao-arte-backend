from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db
from routers.usuario import rota as usuario_rota
from routers.evento import rota as evento_rota


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


app.include_router(usuario_rota)
app.include_router(evento_rota)
