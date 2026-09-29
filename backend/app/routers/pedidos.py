from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.dependencies import exigir_admin, get_db, obter_usuario_atual
from app.models import StatusPedido
from app.schemas import AtualizarStatus, CriarPedido
from app.services.pedido_service import criar_pedido, mudar_status

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/", status_code=201)
def criar_pedido_endpoint(
    pedidocriar: CriarPedido,
    usuario: dict = Depends(obter_usuario_atual),
    db: Session = Depends(get_db),
):
    try:
        return criar_pedido(db, usuario["id"], pedidocriar)
    except HTTPException:
        db.rollback()
        raise
    except OperationalError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao criar pedido no banco de dados")


@router.put("/{id}/status")
def atualizar_status_pedido(
    id: int,
    status: AtualizarStatus,
    admin: dict = Depends(exigir_admin),
    db: Session = Depends(get_db),
):
    try:
        return mudar_status(db, id, status.status)
    except HTTPException:
        db.rollback()
        raise
    except OperationalError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Não foi possivel atualizar o status")