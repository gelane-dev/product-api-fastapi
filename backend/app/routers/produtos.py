from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.dependencies import exigir_admin, get_db
from app.models import Produto
from app.schemas import AtualizarProduto, CriarProduto

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.get("/")
def buscar_produtos(db: Session = Depends(get_db)):
    try:
        buscar = db.query(Produto).all()
        if not buscar:
            raise HTTPException(status_code=404, detail="produto não encontrado")
        return buscar
    except HTTPException:
        raise
    except OperationalError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao consultar o banco de dados")


@router.post("/", status_code=201)
def criar_produtos(
    produto: CriarProduto,
    admin: dict = Depends(exigir_admin),
    db: Session = Depends(get_db),
):
    try:
        if produto.estoque < 0:
            raise HTTPException(status_code=400, detail="Estoque não pode ser menor que 0")
        if produto.preco < 0:
            raise HTTPException(status_code=400, detail="preco não pode ser menor que 0")

        criar = Produto(
            name=produto.name,
            categoria=produto.categoria,
            preco=produto.preco,
            estoque=produto.estoque,
            data_criacao=datetime.now(),
        )
        db.add(criar)
        db.commit()
        return {"mensagem": "produto criado com sucesso"}
    except HTTPException:
        raise
    except OperationalError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao criar produto no banco de dados")


@router.put("/{id}")
def atualizar_produtos(
    id: int,
    produto: AtualizarProduto,
    admin: dict = Depends(exigir_admin),
    db: Session = Depends(get_db),
):
    try:
        alteracao = db.query(Produto).filter(Produto.id == id).first()
        if alteracao is None:
            raise HTTPException(status_code=404, detail="produto não encontrado")
        if produto.estoque is not None and produto.estoque > 1000:
            raise HTTPException(status_code=400, detail="Estoque muito alto")
        if produto.estoque is not None and produto.estoque < 0:
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


@router.delete("/{id}")
def deletar_produtos(
    id: int,
    admin: dict = Depends(exigir_admin),
    db: Session = Depends(get_db),
):
    try:
        deletar = db.query(Produto).filter(Produto.id == id).first()
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