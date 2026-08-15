from fastapi import FastAPI, HTTPException, Depends
from schemas import criarproduto, atualizarproduto, criarusuarios, criarpedido, atualizarstatus, loginschema
from datetime import datetime
from auth import hash_senha, verificar_senha, criar_token, obter_usuario_atual, exigir_admin
from models import statuspedido, usuario, statuspedido, produtos, pedido, itenspedidos
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

app = FastAPI()

transicoes_validas = {
    statuspedido.PENDENTE: [ statuspedido.PAGO, statuspedido.CANCELADO],
    statuspedido.PAGO: [statuspedido.PENDENTE, statuspedido.ENVIADO, statuspedido.CANCELADO],
    statuspedido.ENVIADO : [statuspedido.PAGO],
    statuspedido.CANCELADO : []
}

@app.post("/login/")
def login(credenciais: loginschema, db: Session = Depends(get_db)):

    try:

        usuario_login = db.query(usuario).filter(usuario.email == credenciais.email).first()

        if usuario_login is None:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        if not verificar_senha(credenciais.senha, usuario_login.senha):
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        token = criar_token({"role": usuario_login.role, "sub": usuario_login.email, "id": usuario_login.id})

        return {"access_token": token, "token_type": "bearer"}

    except HTTPException:
        raise
    except  OperationalError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao consultar o banco de dados")
   
@app.post("/cadastro/",status_code = 201)
def criar_usuario(usuarios: criarusuarios, db: Session = Depends(get_db)):

    try:

        cadastrar = usuario(name=usuarios.name, email=usuarios.email, senha=hash_senha(usuarios.senha))
        db.add(cadastrar)
        db.commit()

        return {"mensagem":"usuario criado com sucesso"}

    except HTTPException:
        raise
    except OperationalError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao criar usuário no banco de dados")

@app.get("/produtos/")
def buscar_produtos(db: Session = Depends(get_db)):

    try:

        buscar = db.query(produtos).all()

        if not buscar:
            raise HTTPException(status_code = 404, detail = "produto não encontrado")
        
        return buscar
    
    except HTTPException:
        raise
    except OperationalError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao consultar o banco de dados")

@app.post("/produtos/",status_code = 201)
def criar_produtos(produto: criarproduto, usuario: dict = Depends(exigir_admin), db: Session = Depends(get_db)):

    try:

        if produto.estoque < 0:
            raise HTTPException(status_code=400, detail="Estoque não pode ser menor que 0")
            
        if produto.preco < 0:
            raise HTTPException(status_code=400, detail="preco não pode ser menor que 0")

        criar = produtos(name=produto.name, categoria=produto.categoria, preco=produto.preco, estoque=produto.estoque, data_criacao=datetime.now())

        db.add(criar)
        db.commit()

        return {"mensagem": "produto criado com sucesso"}

    except HTTPException:
        raise
    except OperationalError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao criar produto no banco de dados")

@app.put("/produtos/{id}")
def atualizar_produtos(id: int, produto: atualizarproduto, usuario: dict = Depends(exigir_admin), db: Session = Depends(get_db)):

    try:
        alteracao = db.query(produtos).filter(produtos.id == id).first()

        if alteracao is None:
            raise HTTPException(status_code = 404, detail = "produto não encontrado")

        if produto.estoque is not None and produto.estoque > 1000:
            raise HTTPException(status_code=400, detail="Estoque muito alto")

        if produto.estoque is not None and produto.estoque  < 0:
            raise HTTPException(status_code=400, detail="Estoque não pode ser menor que 0")

        if produto.preco is not None and produto.preco < 0:
            raise HTTPException(status_code=400, detail="preco não pode ser menor que 0")

        if produto.name is not None:
            alteracao.name = produto.name

        if produto.categoria is not None:
            alteracao.categoria = produto.categoria

        if produto.preco is not None:
            alteracao.preco = produto.preco

        if produto.estoque is not None:
            alteracao.estoque = produto.estoque

        db.add(alteracao)
        db.commit()

        return {"mensagem": "Produto atualizado com sucesso"}

    except HTTPException:
        raise
    except OperationalError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar produto no banco de dados")
    
@app.delete("/produtos/{id}")
def deletar_produtos(id: int, usuario: dict = Depends(exigir_admin), db: Session = Depends(get_db)):

    try:
        deletar = db.query(produtos).filter(produtos.id == id).first()

        if deletar is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        db.delete(deletar)
        db.commit()

        return {"mensagem": "Produto deletado com sucesso"}
    
    except HTTPException:
        raise
    except OperationalError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao deletar produto no banco de dados")

@app.post("/pedidos/", status_code=201)
def criar_pedido(pedidocriar: criarpedido, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):

    try:
        itens_calculados =[]
        for item in pedidocriar.itens:
            produto_db = db.query(produtos).filter(produtos.id == item.produto_id).first()

            if produto_db is None:
                raise HTTPException(status_code = 404, detail = "produto não encontrado")
            
            if produto_db.estoque < item.quantidade:
                raise HTTPException(status_code=400, detail="estoque menor que quantidade pedida")

            valor = produto_db.preco * item.quantidade

            itens_calculados.append({
                "produto": produto_db,
                "quantidade": item.quantidade,
                "preco":  produto_db.preco,
                "valor": valor
            })

        total = sum(item_calc["valor"] for item_calc in itens_calculados)
        novo_pedido = pedido(usuario_id=usuario["id"], total=total)

        db.add(novo_pedido)
        db.flush()

        for item_calc in itens_calculados: 
            novo_item = itenspedidos(
                pedidos_id=novo_pedido.id,
                produto_id=item_calc["produto"].id,
                quantidade=item_calc["quantidade"],
                preco_unitario=item_calc["preco"]
            )
            db.add(novo_item)
            item_calc["produto"].estoque -= item_calc["quantidade"]

        db.commit()

        return {"mensagem": "Pedido criado com sucesso", "pedido_id": novo_pedido.id, "total": total}

    except HTTPException:
        db.rollback()
        raise
    except OperationalError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao criar pedido no banco de dados")
 
@app.put("/pedidos/{id}/status")
def atualizar_status_pedido(id: int, status: atualizarstatus, usuario: dict = Depends(exigir_admin), db: Session = Depends(get_db)):

    try:
        pedido_db = db.query(pedido).filter(pedido.id == id).first()
            
        if pedido_db is None:
            raise HTTPException(status_code = 404, detail = "pedido não encontrado")

        if status.status not in transicoes_validas[pedido_db.status]:
            raise HTTPException(status_code = 400, detail = f"Não é possível mudar de '{pedido_db.status}' para '{status.status}'")

        pedido_db.status = status.status

        if status.status == statuspedido.CANCELADO:
             for item in pedido_db.itens:
                item.produto.estoque += item.quantidade

        db.commit()
        return {"mensagem": "status atualizado com sucesso!"}

    except HTTPException:
        db.rollback()
        raise
    except OperationalError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Não foi possivel atualizar o status")
    
    
    
    

   

    



    