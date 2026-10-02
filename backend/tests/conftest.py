import os
 
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from app.core.database import Base
from app.core.security import hash_senha
from app.dependencies import get_db
from app.main import app
from app.models import Usuario, Produto, Pedido, ItemPedido
 
DATABASE_URL_TESTE = os.getenv("DATABASE_URL_TESTE")
 
assert DATABASE_URL_TESTE and DATABASE_URL_TESTE.endswith("_test")
 
engine_teste = create_engine(DATABASE_URL_TESTE)
 
SessionTeste = sessionmaker(
    bind=engine_teste,
    autoflush=False,
    autocommit=False,
)
 
 
@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine_teste)
 
    sessao = SessionTeste()
 
    try:
        yield sessao
    finally:
        sessao.close()
        Base.metadata.drop_all(bind=engine_teste)
 
 
@pytest.fixture
def cliente(db):
    def obter_db_teste():
        yield db
 
    app.dependency_overrides[get_db] = obter_db_teste
 
    with TestClient(app) as cliente_teste:
        yield cliente_teste
 
    app.dependency_overrides.clear()
 
 
@pytest.fixture
def usuario_cliente(db):
    usuario = Usuario(
        name="leonardo",
        email="leo@gmail.com",
        senha=hash_senha("senha123"),
    )
    db.add(usuario)
    db.commit()
    return usuario
 
 
@pytest.fixture
def usuario_admin(db):
    usuario = Usuario(
        name="Admin Teste",
        email="admin@gmail.com",
        senha=hash_senha("admin123"),
        role="admin",
    )
    db.add(usuario)
    db.commit()
    return usuario
 
 
def _headers_de(cliente, email, senha):
    resp = cliente.post("/login/", json={"email": email, "senha": senha})
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}
 
 
@pytest.fixture
def headers_cliente(cliente, usuario_cliente):
    return _headers_de(cliente, "leo@gmail.com", "senha123")
 
 
@pytest.fixture
def headers_admin(cliente, usuario_admin):
    return _headers_de(cliente, "admin@gmail.com", "admin123")


@pytest.fixture
def produto(db):
    produto = Produto(
        name="panela",
        categoria="cozinha",
        preco= 100,
        estoque= 10,
    )
    db.add(produto)
    db.commit()
    return produto

@pytest.fixture
def pedido(db, usuario_cliente, produto):
    pedido = Pedido(
        usuario_id=usuario_cliente.id,
        total=100,
    )

    item = ItemPedido(
        quantidade=1,
        preco_unitario=produto.preco,
        produto_id=produto.id,
    )

    pedido.itens.append(item)

    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    return pedido