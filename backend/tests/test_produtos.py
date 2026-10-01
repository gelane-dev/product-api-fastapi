from app.models import Produto

def  test_cliente_nao_pode_criar_produto(cliente, headers_cliente, db):
    resp = cliente.post("/produtos/", 
    headers=headers_cliente, 
    json={  
        "name": "panela",
        "categoria": "cozinha",
        "preco": 100,
        "estoque": 10,
    })

    verificar = db.query(Produto).count()
    
    assert resp.status_code == 403
    assert verificar == 0 


def test_admin_criar_produto(cliente, headers_admin, db):
    resp = cliente.post("/produtos/", 
    headers=headers_admin, 
    json={  
        "name": "panela",
        "categoria": "cozinha",
        "preco": 100,
        "estoque": 10,
    })

    verificar = db.query(Produto).filter(
        Produto.name == "panela"
        ).first()

    assert resp.status_code == 201
    assert verificar is not None
    assert verificar.name == "panela"
    assert verificar.categoria == "cozinha"
    assert verificar.preco == 100
    assert verificar.estoque == 10


def test_admin_atualizar_produto(cliente, headers_admin, produto, db):
    resp = cliente.put(f"/produtos/{produto.id}", 
    headers=headers_admin, 
    json={  
        "name": "panela inox",
        "categoria": "cozinha",
        "preco": 150,
        "estoque": 20,
    })

    verificar = db.query(Produto).filter(
        Produto.name == "panela inox"
        ).first()
    
    assert resp.status_code == 200
    assert verificar is not None
    assert verificar.name == "panela inox"
    assert verificar.categoria == "cozinha"
    assert verificar.preco == 150
    assert verificar.estoque == 20


def test_admin_deletar_produto(cliente, headers_admin, produto, db):
    resp = cliente.delete(f"/produtos/{produto.id}",
    headers=headers_admin 
    )

    verificar = db.query(Produto).filter(
        Produto.name == "panela"
        ).first()
    
    assert resp.status_code == 200
    assert verificar is None


def test_admin_atualizar_produto_inexistente(cliente, headers_admin):
    resp = cliente.put("/produtos/999", 
    headers=headers_admin, 
    json={  
        "name": "panela inox",
        "categoria": "cozinha",
        "preco": 150,
        "estoque": 20,
    })

    assert resp.status_code == 404


def test_admin_deletar_produto_inexistente(cliente, headers_admin):
    resp = cliente.delete("/produtos/999",
    headers=headers_admin
    )

    assert resp.status_code == 404


def test_usuario_nao_autenticado(cliente):
    resp = cliente.post("/produtos/", 
    json={  
        "name": "panela",
        "categoria": "cozinha",
        "preco": 100,
        "estoque": 10,
    })

    assert resp.status_code == 401