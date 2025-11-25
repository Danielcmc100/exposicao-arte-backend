"""Aplicação principal FastAPI."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db
from routers.avaliacoes_eventos import rota as avaliacoes_eventos_rota
from routers.avaliacoes_obras import rota as avaliacoes_obras_rota
from routers.categoria import rota as categoria_rota
from routers.comentario_evento import rota as comentario_evento_rota
from routers.comentario_obra import rota as comentario_obra_rota
from routers.evento import rota as evento_rota
from routers.link_rede import rota as link_rede_rota
from routers.obra import rota as obra_rota
from routers.obra_evento import rota as obra_evento_rota
from routers.usuario import rota as usuario_rota


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:  # noqa: RUF029
    """Gerencia o ciclo de vida da aplicação.

    Args:
        _app: Instância da aplicação FastAPI (não utilizado).

    Yields:
        None: Controle de execução durante o ciclo de vida.

    """
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root() -> dict[str, str]:
    """Endpoint raiz da API.

    Returns:
        dict: Mensagem de boas-vindas.

    """
    return {"message": "Hello, World!"}


app.include_router(usuario_rota)
app.include_router(link_rede_rota)
app.include_router(categoria_rota)
app.include_router(evento_rota)
app.include_router(comentario_evento_rota)
app.include_router(comentario_obra_rota)
app.include_router(obra_rota)
app.include_router(avaliacoes_eventos_rota)
app.include_router(avaliacoes_obras_rota)
app.include_router(obra_evento_rota)
