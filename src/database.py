"""Configuração e gerenciamento do banco de dados."""

from collections.abc import Generator
from typing import Any

from sqlmodel import Session, SQLModel, create_engine

from config import settings

engine = create_engine(settings.database_url)


def init_db() -> None:
    """Inicializa o banco de dados criando todas as tabelas."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, Any, None]:
    """Cria uma sessão do banco de dados.

    Yields:
        Session: Sessão do banco de dados para realizar operações.

    """
    with Session(engine) as session:
        yield session
