from alembic import command
from alembic.config import Config
import pytest
from sqlalchemy import inspect
from sqlalchemy.engine import Engine


def test_repeated_upgrades(
    sqlite_engine: Engine, alembic_config: Config
) -> None:
    """Testa se podemos executar upgrade múltiplas vezes sem erros."""
    # Primeira execução
    with sqlite_engine.begin() as connection:
        alembic_config.attributes["connection"] = connection
        command.upgrade(alembic_config, "head")

    # Segunda execução (deve ser idempotente)
    with sqlite_engine.begin() as connection:
        alembic_config.attributes["connection"] = connection
        command.upgrade(alembic_config, "head")

    inspector = inspect(sqlite_engine)
    tables = inspector.get_table_names()
    assert "usuarios" in tables


@pytest.mark.integration
def test_partial_migrations(
    postgres_engine: Engine, alembic_config: Config
) -> None:
    """Testa migrações parciais (upgrade até uma revisão específica)."""
    # Upgrade até a primeira migração
    with postgres_engine.begin() as connection:
        alembic_config.attributes["connection"] = connection
        command.upgrade(
            alembic_config, "41590745c3be"
        )  # create users table

    inspector = inspect(postgres_engine)
    tables = inspector.get_table_names()
    assert "usuarios" in tables
    assert "eventos" not in tables  # Ainda não foi criada

    # Continuar upgrade
    with postgres_engine.begin() as connection:
        alembic_config.attributes["connection"] = connection
        command.upgrade(alembic_config, "head")

    # Refresh inspector to see new tables
    inspector = inspect(postgres_engine)
    tables = inspector.get_table_names()
    assert "eventos" in tables