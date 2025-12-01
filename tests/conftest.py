"""Configuração de fixtures do pytest."""

import logging
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from testcontainers.postgres import PostgresContainer

from src.app import app

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


@pytest.fixture
def client(postgres_container: PostgresContainer) -> TestClient:
    return TestClient(app)


@pytest.fixture
def app_with_db(
    postgres_container: PostgresContainer,
    alembic_config: Config,
) -> Generator[TestClient, None, None]:
    """Cria uma aplicação FastAPI com banco PostgreSQL testcontainer.

    Esta fixture:
    1. Cria um container PostgreSQL
    2. Executa as migrations do Alembic
    3. Configura a aplicação para usar o banco de teste
    4. Retorna um TestClient pronto para testes

    Args:
        postgres_container: Container PostgreSQL do testcontainers
        alembic_config: Configuração do Alembic

    Yields:
        TestClient: Cliente de teste da aplicação FastAPI

    """
    import os  # noqa: PLC0415
    import sys  # noqa: PLC0415
    from pathlib import Path  # noqa: PLC0415

    # Adicionar src ao path para resolver imports
    src_path = Path(__file__).parent.parent / "src"
    sys.path.insert(0, str(src_path))

    # Obter URL de conexão do container
    db_url = postgres_container.get_connection_url()

    # Configurar variável de ambiente antes de importar a aplicação
    os.environ["DATABASE_URL"] = db_url

    # Limpar módulos já importados do src para evitar conflito de metadata
    modules_to_remove = [
        key
        for key in sys.modules
        if key.startswith(("config", "database", "models", "routers", "app"))
    ]
    for module in modules_to_remove:
        del sys.modules[module]

    # Executar migrations
    alembic_config.set_main_option("sqlalchemy.url", db_url)
    command.upgrade(alembic_config, "head")

    # Importar a aplicação após configurar o banco e limpar imports
    from app import app  # noqa: PLC0415

    # Criar cliente de teste
    client = TestClient(app)

    yield client

    # Cleanup
    sys.path.remove(str(src_path))
    if "DATABASE_URL" in os.environ:
        del os.environ["DATABASE_URL"]
