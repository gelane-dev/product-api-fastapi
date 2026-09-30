import pytest
from app.models import Usuario

def test_cadastro_sucesso(cliente, db):
    resp = cliente.post("/cadastro/", json={
        "name": "leonardo",
        "email": "leo@gmail.com",
        "senha": "senha123",
    })

    assert resp.status_code == 201
    assert resp.json()["mensagem"] == "Usuário criado com sucesso"
    assert db.query(Usuario).count() == 1


def test_cadastro_email_duplicado(cliente, usuario_cliente, db):
    resp = cliente.post("/cadastro/", json={
        "name": "leonardo",
        "email": "leo@gmail.com",
        "senha": "senha123",
    })

    contagem = db.query(Usuario).count()

    assert resp.status_code == 409
    assert contagem == 1


@pytest.mark.parametrize("name, email, senha", [
    ("le", "leo@gmail.com", "senha123"),
    ("leonardo", "leo", "senha123"),
    ("leonardo", "leo@gmail.com", "123"),
], ids=["nome_curto", "email_invalido", "senha_curta"])


def test_cadastro_dados_invalidos(cliente, name, email, senha):
    resp = cliente.post("/cadastro/", json={
        "name": name,
        "email": email,
        "senha": senha,
    })

    assert resp.status_code == 422


def test_login_sucesso(cliente, usuario_cliente):
    resp = cliente.post("/login/", json={
        "email": "leo@gmail.com",
        "senha": "senha123",
    })

    assert resp.status_code == 200
    assert resp.json()["token_type"] == "bearer"
    assert resp.json()["access_token"]


def test_login_senha_errada(cliente, usuario_cliente):
    resp = cliente.post("/login/", json={
        "email": "leo@gmail.com",
        "senha": "errada",
    })

    assert resp.status_code == 401


def test_login_usuario_inexistente(cliente, db):
    resp = cliente.post("/login/", json={
        "email": "naoexiste@gmail.com",
        "senha": "senha123",
    })

    usuario = db.query(Usuario).filter(Usuario.email == "naoexiste@gmail.com").first()

    assert resp.status_code == 401
    assert usuario is None
    assert resp.json()["detail"] == "Credenciais inválidas"