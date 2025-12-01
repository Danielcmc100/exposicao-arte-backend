from fastapi.testclient import TestClient



# teste
def test_criar_usuario_completo(client: TestClient) -> None:
    payload = {
        "nome": "Vincent van Gogh",
        "email": "vincent@arte.com",
        "senha": "123456_super_secreta",
        "funcao": 2,
        "biografia": "Pintor pós-impressionista holandês.",
    }

    response = client.post("/usuarios/", json=payload)

    assert response.status_code in [200, 201]

    data = response.json()

    # Verifica se os dados voltaram corretos
    assert data["nome"] == "Vincent van Gogh"
    assert data["email"] == "vincent@arte.com"
    assert data["funcao"] == 2
    assert data["biografia"] == "Pintor pós-impressionista holandês."
