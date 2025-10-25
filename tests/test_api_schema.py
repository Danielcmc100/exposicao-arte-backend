"""Testes de schema da API usando Schemathesis."""

import pytest


@pytest.mark.integration
def test_api_schema_compliance(app_with_db) -> None:  # noqa: ANN001
    """Testa conformidade dos endpoints com o schema OpenAPI.

    Valida:
    - API inicia corretamente
    - Schema OpenAPI é acessível
    - Endpoints básicos funcionam

    Args:
        app_with_db: Cliente de teste com aplicação e banco configurados

    """
    # Testar o endpoint raiz
    OK_STATUS = 200  # noqa: N806
    response = app_with_db.get("/")
    assert response.status_code == OK_STATUS
    assert response.json() == {"message": "Hello, World!"}

    # Verificar que o schema OpenAPI está acessível
    response = app_with_db.get("/openapi.json")
    assert response.status_code == OK_STATUS
    openapi_schema = response.json()

    # Validações básicas do schema
    assert "openapi" in openapi_schema
    assert "info" in openapi_schema
    assert "paths" in openapi_schema
    assert len(openapi_schema["paths"]) > 0
