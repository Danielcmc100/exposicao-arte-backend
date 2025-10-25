# Testes

Este diretório contém os testes automatizados do backend.

## Estrutura

- `conftest.py`: Configuração de fixtures do pytest
- `test_migrations.py`: Testes de migração do Alembic para SQLite e PostgreSQL

## Executando os testes

### Instalar dependências de desenvolvimento

```bash
uv sync --all-groups
```

### Executar todos os testes (SQLite apenas)

Por padrão, apenas os testes do SQLite são executados:

```bash
uv run pytest
```

### Executar incluindo testes de integração (PostgreSQL)

Os testes marcados com `@pytest.mark.integration` usam **testcontainers** para criar automaticamente um container PostgreSQL durante os testes. **Não é necessário ter PostgreSQL instalado ou rodando!**

Requisito: Docker deve estar instalado e rodando.

```bash
# Executar todos os testes incluindo PostgreSQL
uv run pytest -m "integration or not integration"

# Ou simplesmente
uv run pytest --override-ini="addopts="
```

### Pular testes de integração

```bash
uv run pytest -m "not integration"
```

### Executar apenas testes de migração

```bash
uv run pytest tests/test_migrations.py
```

### Executar testes específicos

```bash
# Apenas SQLite
uv run pytest tests/test_migrations.py::TestMigrations::test_sqlite_migrations

# Apenas PostgreSQL
uv run pytest tests/test_migrations.py::TestMigrations::test_postgres_migrations

# Teste de consistência entre bancos
uv run pytest tests/test_migrations.py::TestMigrations::test_migration_consistency
```

### Executar com saída detalhada

```bash
uv run pytest -v -s
```

## Requisitos

### Para testes SQLite
- Nenhum requisito adicional (SQLite é embutido no Python)

### Para testes PostgreSQL (com testcontainers)
- Docker instalado e rodando
- Testcontainers cria e gerencia automaticamente containers PostgreSQL temporários
- Não é necessário ter PostgreSQL instalado localmente!

## O que é testado

### Testes de Migração (`TestMigrations`)

1. **test_sqlite_migrations**: Testa o ciclo completo de upgrade/downgrade no SQLite
2. **test_postgres_migrations**: Testa o ciclo completo de upgrade/downgrade no PostgreSQL
3. **test_migration_consistency**: Verifica se ambos os bancos produzem esquemas consistentes

### Testes de Robustez (`TestMigrationRobustness`)

1. **test_repeated_upgrades**: Verifica se múltiplas execuções de upgrade são seguras
2. **test_partial_migrations**: Testa migrações parciais até revisões específicas

## Verificações realizadas

- ✅ Criação de todas as tabelas esperadas
- ✅ Existência de todas as colunas necessárias
- ✅ Tipos ENUM criados corretamente (PostgreSQL)
- ✅ Downgrade remove todas as tabelas
- ✅ Idempotência das migrações
- ✅ Consistência entre SQLite e PostgreSQL
