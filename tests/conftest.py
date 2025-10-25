"""Configuração de fixtures do pytest."""

import logging
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from testcontainers.postgres import PostgresContainer

# Configurar logging para testes
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


@pytest.fixture
def alembic_config() -> Config:
    """Retorna a configuração do Alembic.

    Returns:
        Config: Configuração do Alembic com caminhos corretos.

    """
    project_root = Path(__file__).parent.parent
    alembic_ini_path = project_root / "alembic.ini"

    config = Config(str(alembic_ini_path))
    config.set_main_option("script_location", str(project_root / "migrations"))

    return config


@pytest.fixture
def sqlite_engine() -> Generator[Engine, None, None]:
    """Cria um engine SQLite temporário para testes.

    Yields:
        Engine: Engine SQLite configurado e pronto para uso.

    """
    # Criar um arquivo temporário para o banco SQLite
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_file:
        db_path = tmp_file.name

    database_url = f"sqlite:///{db_path}"
    engine = create_engine(database_url)

    yield engine

    # Cleanup
    engine.dispose()
    if Path(db_path).exists():
        Path(db_path).unlink()


@pytest.fixture(scope="module")
def postgres_container() -> Generator[PostgresContainer, None, None]:
    """Cria um container PostgreSQL usando testcontainers.

    Seguindo o padrão da documentação oficial.
    Scope 'module' significa que o container é compartilhado entre
    testes do mesmo módulo.

    Yields:
        PostgresContainer: Container PostgreSQL iniciado e pronto.

    """
    postgres = PostgresContainer("postgres:16-alpine")
    postgres.start()

    yield postgres

    postgres.stop()


@pytest.fixture
def postgres_engine(
    postgres_container: PostgresContainer,
) -> Generator[Engine, None, None]:
    """Cria um engine PostgreSQL conectado ao container de teste.

    Seguindo o exemplo da documentação oficial do testcontainers.
    Cada teste recebe um engine limpo.

    Yields:
        Engine: Engine PostgreSQL configurado e conectado.

    """
    # Obter connection string do container
    connection_url = postgres_container.get_connection_url()

    # Criar engine
    engine = create_engine(connection_url)

    # Verificar conexão
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        version = result.fetchone()
        if version:
            message = f"✅ PostgreSQL conectado: {version[0][:50]}..."
            logger.info(message)

    yield engine

    # Cleanup: Drop e recria schema public (remove tudo: tabelas, tipos, etc)
    with engine.begin() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))

    engine.dispose()
