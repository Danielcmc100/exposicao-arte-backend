"""Testes de migração do Alembic para SQLite e PostgreSQL."""

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine



def _run_migrations(
     engine: Engine, alembic_config: Config, revision: str = "head"
) -> None:
    """Executa as migrações do Alembic em um engine específico."""
    # Configurar a URL do banco no alembic config
    alembic_config.set_main_option("sqlalchemy.url", str(engine.url))

    # Executar upgrade
    command.upgrade(alembic_config, revision)

def _verify_tables_exist( engine: Engine) -> None:
    """Verifica se todas as tabelas esperadas foram criadas."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    expected_tables = [
        "usuarios",
        "eventos",
        "categorias",
        "obras",
        "link_redes",
        "comentario_obras",
        "comentario_eventos",
        "alembic_version",
    ]

    for table in expected_tables:
        assert table in tables, f"Tabela '{table}' não foi criada"

def _verify_usuarios_columns( engine: Engine) -> None:
    """Verifica se a tabela usuarios tem todas as colunas esperadas."""
    inspector = inspect(engine)
    columns = {col["name"] for col in inspector.get_columns("usuarios")}

    expected_columns = {
        "id",
        "nome",
        "email",
        "senha",
        "funcao",
        "biografia",
    }

    assert expected_columns.issubset(columns), (
        f"Colunas faltando: {expected_columns - columns}"
    )

def _verify_enum_values( engine: Engine, db_type: str) -> None:
    """Verifica se os valores ENUM estão corretos."""
    if db_type == "postgresql":
        # No PostgreSQL, podemos verificar o tipo ENUM diretamente
        with engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT enumlabel FROM pg_enum "
                    "WHERE enumtypid = 'funcao'::regtype "
                    "ORDER BY enumlabel"
                )
            )
            enum_values = {row[0] for row in result}
            expected_values = {"ADMIN", "ARTISTA", "CONSUMIDOR"}
            assert enum_values == expected_values, (
                f"Valores ENUM incorretos: {enum_values}"
            )
    elif db_type == "sqlite":
        # No SQLite, verificamos se a coluna aceita os valores
        # (SQLite não tem ENUMs nativos, então apenas verificamos a coluna)
        inspector = inspect(engine)
        columns = inspector.get_columns("usuarios")
        funcao_col = next(
            (col for col in columns if col["name"] == "funcao"), None
        )
        assert funcao_col is not None, "Coluna 'funcao' não encontrada"

def _test_full_migration_cycle(
     engine: Engine, alembic_config: Config, db_type: str
) -> None:
    """Testa o ciclo completo de upgrade e downgrade."""
    # Configure Alembic to use the provided engine's connection
    alembic_config.attributes["connection"] = engine

    print(f"🔧 Usando engine existente: {engine.url}")

    # Verificar a versão atual antes do upgrade
    from alembic.runtime.migration import MigrationContext

    with engine.connect() as conn:
        context = MigrationContext.configure(conn)
        current_rev = context.get_current_revision()
        print(f"Revisão atual antes do upgrade: {current_rev}")

    # Teste de upgrade
    print("⬆️  Executando upgrade...")
    with engine.begin() as connection:
        alembic_config.attributes["connection"] = connection
        command.upgrade(alembic_config, "head")

    # Verificar versão após upgrade
    with engine.connect() as conn:
        context = MigrationContext.configure(conn)
        current_rev = context.get_current_revision()
        print(f"Revisão atual após o upgrade: {current_rev}")

    # Verificar que as tabelas foram criadas
    _verify_tables_exist(engine)
    _verify_usuarios_columns(engine)
    _verify_enum_values(engine, db_type)

    # Teste de downgrade
    print("⬇️  Executando downgrade...")
    with engine.begin() as connection:
        alembic_config.attributes["connection"] = connection
        command.downgrade(alembic_config, "base")

    # Verificar que as tabelas foram removidas (exceto alembic_version)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    user_tables = [t for t in tables if t != "alembic_version"]
    assert len(user_tables) == 0, (
        f"Tabelas não foram removidas no downgrade: {user_tables}"
    )

    # Teste de upgrade novamente para garantir idempotência
    print("⬆️  Executando upgrade novamente (teste de idempotência)...")
    with engine.begin() as connection:
        alembic_config.attributes["connection"] = connection
        command.upgrade(alembic_config, "head")
    _verify_tables_exist(engine)

def test_sqlite_migrations(
     sqlite_engine: Engine, alembic_config: Config
) -> None:
    """Testa as migrações no SQLite."""
    _test_full_migration_cycle(
        sqlite_engine, alembic_config, "sqlite"
    )

@pytest.mark.integration
def test_postgres_migrations(
     postgres_engine: Engine, alembic_config: Config
) -> None:
    """Testa as migrações no PostgreSQL."""
    _test_full_migration_cycle(
        postgres_engine, alembic_config, "postgresql"
    )

@pytest.mark.integration
def test_migration_consistency(
    
    sqlite_engine: Engine,
    postgres_engine: Engine,
    alembic_config: Config,
) -> None:
    """Testa se as migrações produzem esquemas consistentes
    entre SQLite e PostgreSQL.
    """
    # Aplicar migrações em ambos usando connections
    sqlite_config = Config(alembic_config.config_file_name)
    script_location = alembic_config.get_main_option("script_location")
    if script_location:
        sqlite_config.set_main_option("script_location", script_location)

    with sqlite_engine.begin() as connection:
        sqlite_config.attributes["connection"] = connection
        command.upgrade(sqlite_config, "head")

    postgres_config = Config(alembic_config.config_file_name)
    if script_location:
        postgres_config.set_main_option("script_location", script_location)

    with postgres_engine.begin() as connection:
        postgres_config.attributes["connection"] = connection
        command.upgrade(postgres_config, "head")

    # Comparar tabelas
    sqlite_inspector = inspect(sqlite_engine)
    postgres_inspector = inspect(postgres_engine)

    sqlite_tables = set(sqlite_inspector.get_table_names())
    postgres_tables = set(postgres_inspector.get_table_names())

    assert sqlite_tables == postgres_tables, (
        f"Tabelas diferentes entre bancos: SQLite={sqlite_tables}, PostgreSQL={postgres_tables}"
    )

    # Comparar colunas da tabela usuarios
    sqlite_cols = {
        col["name"] for col in sqlite_inspector.get_columns("usuarios")
    }
    postgres_cols = {
        col["name"] for col in postgres_inspector.get_columns("usuarios")
    }

    assert sqlite_cols == postgres_cols, (
        f"Colunas diferentes na tabela usuarios: SQLite={sqlite_cols}, PostgreSQL={postgres_cols}"
    )



