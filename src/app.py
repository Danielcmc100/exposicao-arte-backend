from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db
from routers.usuario import rota
from routers.categoria import rota


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


app.include_router(rota)
