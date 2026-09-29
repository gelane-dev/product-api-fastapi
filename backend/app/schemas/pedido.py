from pydantic import BaseModel, Field

from app.models import StatusPedido


class ItemPedidoIn(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)


class CriarPedido(BaseModel):
    itens: list[ItemPedidoIn] = Field(min_length=1)


class AtualizarStatus(BaseModel):
    status: StatusPedido