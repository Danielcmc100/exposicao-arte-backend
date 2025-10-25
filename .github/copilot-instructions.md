# Instruções para o GitHub Copilot

## Tecnologias do Projeto

### Stack Principal
- **Python 3.12+** - Linguagem base
- **FastAPI 0.116+** - Framework web assíncrono
- **SQLModel 0.0.24** - ORM (SQLAlchemy + Pydantic)
- **PostgreSQL** - Banco de dados
- **Alembic 1.16+** - Migrações de banco
- **Pydantic Settings 2.10+** - Gerenciamento de configurações

### Ferramentas de Desenvolvimento
- **uv** - Gerenciador de pacotes Python
- **Ruff** - Linter e formatador
- **Pyright 1.1+** - Type checker
- **Pytest 8.3+** - Framework de testes
- **Testcontainers 4.8+** - Testes com containers
- **Schemathesis 4.2+** - Testes de API baseados em propriedades

## Idioma
- **SEMPRE escreva documentações, comentários e docstrings em PORTUGUÊS**
- Nomes de variáveis, funções e classes devem estar em inglês
- Mensagens de commit e comentários de código em português

## Padrões de Código Python
- Use snake_case para funções e variáveis
- Use PascalCase para classes
- **Máximo de 79 caracteres por linha** (conforme Ruff configurado)
- Indentação de 4 espaços
- Use type hints em todas as funções
- Docstrings no formato Google Style **em português**
- Use aspas duplas para strings (`"texto"`)
- Python version: >= 3.12

## Docstrings
- **Args** deve ser utilizado o menos possível (preferir type hints)
- **Raises** só deve ser utilizado quando a função explicitamente lança uma exceção com `raise`
- **Returns** devem ser documentados, exceto quando a função retorna `None`
- **IMPORTANTE**: Docstring deve SEMPRE vir imediatamente APÓS a linha com o fechamento dos parâmetros `)` e o tipo de retorno `:`. A docstring deve ser a PRIMEIRA linha dentro do corpo da função, nunca entre a assinatura `def` e os parâmetros
- Priorize descrições claras e concisas sobre seções desnecessárias

## Formatação (Ruff)
- Line length: 79 caracteres
- Quote style: aspas duplas
- Indent style: espaços (4)
- Docstring code format habilitado
- Sempre organize imports automaticamente

## Estrutura do Projeto
- Models em `src/models/`
- Repositories em `src/repositories/`
- Routers em `src/routers/`
- Services em `src/services/`
- Tests em `tests/`
- Migrations em `migrations/`

## Padrões FastAPI
- Use `Annotated` para dependências
- Sempre inclua status codes nas respostas
- Use Pydantic models para validação
- Inclua descrições nas rotas com `description=` **em português**
- Use SQLModel para modelos de dados

## Boas Práticas
- Evite variáveis dummy sem sentido
- Sempre fixe problemas detectados pelo Ruff quando possível
- Não ignore erros de segurança (S101, S404, etc já estão configurados)
- Use preview features do Ruff
- Exclua `migrations` e `venv` da análise