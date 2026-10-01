from app.models import ItemPedido, Produto, Pedido

def test_estoque_insuficiente(cliente, headers_cliente, db, produto):
    resp = cliente.post("/pedidos/", 
    headers=headers_cliente, 
    json={  
        "itens":[
            {
                "produto_id": produto.id,
                "quantidade": 11,
            }
        ]
    },
)
    contagem = db.query(ItemPedido).count()

    assert resp.status_code == 400
    assert contagem == 0


def test_pedido_criado_sucesso(cliente, headers_cliente, produto, db):
    resp = cliente.post("/pedidos/", 
    headers=headers_cliente, 
    json={  
        "itens":[
            {
                "produto_id": produto.id,
                "quantidade": 1,
            }
        ]
    },
)
    verificar = db.query(ItemPedido).filter(
        ItemPedido.produto_id == produto.id
        ).count()
    
    produto_encontrado = db.query(Produto).filter(
        Produto.id == produto.id
        ).first()
    
    assert resp.status_code == 201
    assert verificar == 1
    assert produto_encontrado.estoque == 9

    
def test_produto_inexistente(cliente, headers_cliente):
    resp = cliente.post("/pedidos/",
    headers=headers_cliente, 
    json={  
        "itens":[
            {
                "produto_id": 999,
                "quantidade": 10,
            }
        ]
    },
)

    assert resp.status_code == 404


def test_criar_pedido_quantidade_zero(cliente, headers_cliente, produto):
    resp = cliente.post("/pedidos/", 
    headers=headers_cliente, 
    json={  
        "itens":[
            {
                "produto_id": produto.id,
                "quantidade": 0,
            }
        ]
    },
)
   
    assert resp.status_code == 422


def test_criar_pedido_quantidade_negativa(cliente, headers_cliente, produto):
    resp = cliente.post("/pedidos/", 
    headers=headers_cliente, 
    json={  
        "itens":[
            {
                "produto_id": produto.id,
                "quantidade": -1,
            }
        ]
    },
)
   
    assert resp.status_code == 422


def test_criar_pedido_sem_itens(cliente, headers_cliente):
    resp = cliente.post("/pedidos/", 
    headers=headers_cliente, 
    json={  
        "itens":[]
    },
)

    assert resp.status_code == 422


def test_criar_pedido_calcula_total(cliente, headers_cliente, produto, db):
    resp = cliente.post("/pedidos/", 
    headers=headers_cliente, 
    json={  
        "itens":[
            {
                "produto_id": produto.id,
                "quantidade": 2,
            }
        ]
    },
)
    verificar = db.query(Pedido).order_by(Pedido.id.desc()).first()
    
    assert verificar is not None
    assert resp.status_code == 201
    assert verificar.total == 200
    

def  test_criar_pedido_define_preco_unitario(cliente, headers_cliente, produto, db):
    resp = cliente.post("/pedidos/", 
    headers=headers_cliente, 
    json={  
        "itens":[
            {
                "produto_id": produto.id,
                "quantidade": 1,
            }
        ]
    },
)

    verificar = db.query(ItemPedido).filter(
    ItemPedido.produto_id == produto.id
    ).first()

    assert verificar is not None
    assert resp.status_code == 201
    assert verificar.preco_unitario == 100
    