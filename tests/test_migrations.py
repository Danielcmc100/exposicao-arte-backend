"""Testes de migração do Alembic para SQLite e PostgreSQL."""

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


class TestMigrations:
    """Testes para validar migrações em diferentes bancos de dados."""

    def _run_migrations(
        self, engine: Engine, alembic_config: Config, revision: str = "head"
    ) -> None:
        """Executa as migrações do Alembic em um engine específico."""
        # Configurar a URL do banco no alembic config
        alembic_config.set_main_option("sqlalchemy.url", str(engine.url))

        # Executar upgrade
        command.upgrade(alembic_config, revision)

    def _verify_tables_exist(self, engine: Engine) -> None:
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

    def _verify_usuarios_columns(self, engine: Engine) -> None:
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

    def _verify_enum_values(self, engine: Engine, db_type: str) -> None:
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
            funcao_col = next((col for col in columns if col["name"] == "funcao"), None)
            assert funcao_col is not None, "Coluna 'funcao' não encontrada"

    def _test_full_migration_cycle(
        self, engine: Engine, alembic_config: Config, db_type: str
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
        self._verify_tables_exist(engine)
        self._verify_usuarios_columns(engine)
        self._verify_enum_values(engine, db_type)

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
        self._verify_tables_exist(engine)

    def test_sqlite_migrations(
        self, sqlite_engine: Engine, alembic_config: Config
    ) -> None:
        """Testa as migrações no SQLite."""
        self._test_full_migration_cycle(sqlite_engine, alembic_config, "sqlite")

    @pytest.mark.integration
    def test_postgres_migrations(
        self, postgres_engine: Engine, alembic_config: Config
    ) -> None:
        """Testa as migrações no PostgreSQL."""
        self._test_full_migration_cycle(postgres_engine, alembic_config, "postgresql")

    @pytest.mark.integration
    def test_migration_consistency(
        self, sqlite_engine: Engine, postgres_engine: Engine, alembic_config: Config
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
        sqlite_cols = {col["name"] for col in sqlite_inspector.get_columns("usuarios")}
        postgres_cols = {
            col["name"] for col in postgres_inspector.get_columns("usuarios")
        }

        assert sqlite_cols == postgres_cols, (
            f"Colunas diferentes na tabela usuarios: SQLite={sqlite_cols}, PostgreSQL={postgres_cols}"
        )


class TestMigrationRobustness:
    """Testes adicionais para robustez das migrações."""

    def test_repeated_upgrades(
        self, sqlite_engine: Engine, alembic_config: Config
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
        self, postgres_engine: Engine, alembic_config: Config
    ) -> None:
        """Testa migrações parciais (upgrade até uma revisão específica)."""
        # Upgrade até a primeira migração
        with postgres_engine.begin() as connection:
            alembic_config.attributes["connection"] = connection
            command.upgrade(alembic_config, "41590745c3be")  # create users table

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
