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