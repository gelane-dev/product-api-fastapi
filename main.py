from fastapi import FastAPI, HTTPException, Depends
from database import conectar
from schemas import criarproduto, atualizarproduto, criarusuarios, criarpedido
from datetime import datetime
import psycopg2
from auth import hash_senha, verificar_senha, criar_token, obter_usuario_atual, exigir_admin

app = FastAPI()

@app.post("/login/")
def login(email:str, senha:str):

    conn = conectar()
    cursor = conn.cursor()

    try:

        cursor.execute('SELECT role, id, email, senha FROM usuarios where email = %s', (email,))
        usuario = cursor.fetchone()

        if usuario is None:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        role_usuario, id_usuario, email_usuario, hash_salvo = usuario

        if not verificar_senha(senha, hash_salvo):
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        token = criar_token({"role": role_usuario, "sub": email_usuario, "id": id_usuario})

        return {"access_token": token, "token_type": "bearer"}

    except HTTPException:
        raise
    except psycopg2.Error:
        raise HTTPException(status_code=500, detail="Erro ao consultar o banco de dados")

    finally:
        cursor.close()
        conn.close()

@app.post("/cadastro/",status_code = 201)
def criar_usuario(usuarios: criarusuarios):

    conn = conectar()
    cursor = conn.cursor()

    try:

        cursor.execute('''INSERT INTO usuarios
            (name,email,senha)
            values (%s,%s,%s)
            ''',(
            usuarios.name,
            usuarios.email,
            hash_senha(usuarios.senha),
            ))

        conn.commit()

        return {"mensagem":"usuario criado com sucesso"}

    except HTTPException:
        raise
    except psycopg2.Error:
        raise HTTPException(status_code=500, detail="Erro ao criar usuário no banco de dados")
    finally:
        cursor.close()
        conn.close()

@app.get("/produtos/")
def buscar_produtos():

    conn = conectar()
    cursor = conn.cursor()

    try:

        cursor.execute('SELECT * FROM produto')
        dados = cursor.fetchall()

        if not dados:
            raise HTTPException(status_code = 404, detail = "produto não encontrado")
        
        return dados
    
    except HTTPException:
        raise
    except psycopg2.Error:
        raise HTTPException(status_code=500, detail="Erro ao consultar o banco de dados")

    finally:
        cursor.close()
        conn.close()

@app.post("/produtos/",status_code = 201)
def criar_produtos(produto: criarproduto, usuario: dict = Depends(exigir_admin)):

    conn = conectar()
    cursor = conn.cursor()

    try:

        if produto.estoque < 0:
            raise HTTPException(status_code=400, detail="Estoque não pode ser menor que 0")
            
        if produto.preco < 0:
            raise HTTPException(status_code=400, detail="preco não pode ser menor que 0")

        cursor.execute('''INSERT INTO produto 
            (name,categoria,preco,estoque,data_criacao)
            values (%s,%s,%s,%s,%s)
            ''',(
            produto.name,
            produto.categoria,
            produto.preco,
            produto.estoque,
            datetime.now()
            ))

        conn.commit()

        return {"produto criado com sucesso"}

    except HTTPException:
        raise
    except psycopg2.Error:
        raise HTTPException(status_code=500, detail="Erro ao criar produto no banco de dados")
    finally:
        cursor.close()
        conn.close()

@app.put("/produtos/{id}")
def atualizar_produtos(id: int, produto: atualizarproduto, usuario: dict = Depends(exigir_admin)):

    conn = conectar()
    cursor = conn.cursor()

    try:

        cursor.execute("SELECT id FROM produto WHERE id = %s", (id,))

        if cursor.fetchone() is None:
            raise HTTPException(status_code = 404, detail = "produto não encontrado")

        if produto.estoque is not None and produto.estoque > 1000:
            raise HTTPException(status_code=400, detail="Estoque muito alto")

        if produto.estoque is not None and produto.estoque  < 0:
            raise HTTPException(status_code=400, detail="Estoque não pode ser menor que 0")

        if produto.preco is not None and produto.preco < 0:
            raise HTTPException(status_code=400, detail="preco não pode ser menor que 0")

        cursor.execute("""
            UPDATE produto
            SET name = %s,
                categoria = %s,
                preco = %s,
                estoque = %s
            WHERE id = %s
        """, (
            produto.name,
            produto.categoria,
            produto.preco,
            produto.estoque,
            id
        ))
    
        conn.commit()
        return {"mensagem": "Produto atualizado com sucesso"}

    except HTTPException:
        raise
    except psycopg2.Error:
        raise HTTPException(status_code=500, detail="Erro ao atualizar produto no banco de dados")
    finally:
        cursor.close()
        conn.close()

@app.delete("/produtos/{id}")
def deletar_produtos(id: int, usuario: dict = Depends(exigir_admin)):

    
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM produto WHERE id = %s", (id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        cursor.execute("DELETE FROM produto WHERE id = %s", (id,))
        
        conn.commit()
        return {"mensagem": "Produto deletado com sucesso"}
    
    except HTTPException:
        raise
    except psycopg2.Error:
        raise HTTPException(status_code=500, detail="Erro ao deletar produto no banco de dados")
    finally:
        cursor.close()
        conn.close()
    

@app.post("/pedidos/", status_code=201)
def criar_pedido(pedido: criarpedido, usuario: dict = Depends(obter_usuario_atual)):

    conn = conectar()
    cursor = conn.cursor()

    try:
        itens_calculados =[]
        for item in pedido.itens:
            cursor.execute("SELECT preco, estoque FROM produto WHERE id = %s", (item.produto_id,))
            resultado = cursor.fetchone()
            
            if resultado is None:
                raise HTTPException(status_code = 404, detail = "produto não encontrado")

            preco, estoque = resultado
            
            if estoque < item.quantidade:
                raise HTTPException(status_code=400, detail="estoque menor que quantidade pedida")

            valor = preco * item.quantidade

            itens_calculados.append({
                "produto_id": item.produto_id,
                "quantidade": item.quantidade,
                "preco": preco,
                "valor": valor
                })
        total = 0
        for item_calc in itens_calculados:
                total = total + item_calc["valor"]

        cursor.execute("""INSERT INTO pedidos (usuarios_id, total) VALUES (%s, %s)
            RETURNING id""", (usuario["id"], total))

        pedido_id = cursor.fetchone()[0]

        for item_cal in itens_calculados:                
            cursor.execute("""INSERT INTO itens_pedidos (pedidos_id, produto_id, quantidade, preco_unitario) 
                        VALUES (%s, %s, %s, %s)
                    """,(
            pedido_id,
            item_cal["produto_id"],
            item_cal["quantidade"],
            item_cal["preco"]
            ))
            cursor.execute("""UPDATE produto SET estoque = estoque - %s WHERE id = %s""",(item_cal["quantidade"], item_cal["produto_id"]))
                    
        conn.commit()
        return {"mensagem": "Pedido criado com sucesso", "pedido_id": pedido_id, "total": total}

    except HTTPException:
        conn.rollback()
        raise
    except psycopg2.Error:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Erro ao criar pedido no banco de dados")
    finally:

        cursor.close()
        conn.close()
    
    
    
    
    
    

   

    



    