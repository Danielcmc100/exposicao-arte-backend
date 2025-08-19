from fastapi import FastAPI

from cachorro import rota

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

app.include_router(rota)