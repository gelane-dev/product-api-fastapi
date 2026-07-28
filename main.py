from fastapi import FastAPI, HTTPException
from database import conectar
from schemas import criarproduto, atualizarproduto
from datetime import datetime
import psycopg2

app = FastAPI()


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
def criar_produtos(produto: criarproduto):

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
def atualizar_produtos(id: int, produto: atualizarproduto):

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
def deletar_produtos(id:int, ):

    
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
    



    



    