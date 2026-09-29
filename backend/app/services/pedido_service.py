from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import ItemPedido, Pedido, Produto, StatusPedido
from app.schemas import CriarPedido

TRANSICOES_VALIDAS = {
    StatusPedido.PENDENTE: [StatusPedido.PAGO, StatusPedido.CANCELADO],
    StatusPedido.PAGO: [StatusPedido.ENVIADO, StatusPedido.CANCELADO],
    StatusPedido.ENVIADO: [],
    StatusPedido.CANCELADO: [],
}


def criar_pedido(db: Session, usuario_id: int, dados: CriarPedido) -> dict:
    itens_calculados = []
    for item in dados.itens:
        produto_db = db.query(Produto).filter(Produto.id == item.produto_id).first()
        if produto_db is None:
            raise HTTPException(status_code=404, detail="produto não encontrado")
        if produto_db.estoque < item.quantidade:
            raise HTTPException(status_code=400, detail="estoque menor que quantidade pedida")
        valor = produto_db.preco * item.quantidade
        itens_calculados.append(
            {
                "produto": produto_db,
                "quantidade": item.quantidade,
                "preco": produto_db.preco,
                "valor": valor,
            }
        )

    total = sum(item_calculado["valor"] for item_calculado in itens_calculados)
    novo_pedido = Pedido(usuario_id=usuario_id, total=total)
    db.add(novo_pedido)
    db.flush()

    for item_calculado in itens_calculados:
        db.add(
            ItemPedido(
                pedidos_id=novo_pedido.id,
                produto_id=item_calculado["produto"].id,
                quantidade=item_calculado["quantidade"],
                preco_unitario=item_calculado["preco"],
            )
        )
        item_calculado["produto"].estoque -= item_calculado["quantidade"]

    db.commit()
    return {
        "mensagem": "Pedido criado com sucesso",
        "pedido_id": novo_pedido.id,
        "total": total,
    }


def mudar_status(db: Session, pedido_id: int, novo_status: StatusPedido) -> dict:
    pedido_db = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if pedido_db is None:
        raise HTTPException(status_code=404, detail="pedido não encontrado")
    if novo_status not in TRANSICOES_VALIDAS[pedido_db.status]:
        raise HTTPException(
            status_code=400,
            detail=(
                "Não é possível mudar de "
                f"'statuspedido.{pedido_db.status.name}' para "
                f"'statuspedido.{novo_status.name}'"
            ),
        )

    pedido_db.status = novo_status
    if novo_status == StatusPedido.CANCELADO:
        for item in pedido_db.itens:
            item.produto.estoque += item.quantidade

    db.commit()
    return {"mensagem": "status atualizado com sucesso!"}