from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class StatusPedido(str, Enum):
    PENDENTE = "pendente"
    PAGO = "pago"
    ENVIADO = "enviado"
    CANCELADO = "cancelado"


class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    usuario: Mapped["Usuario"] = relationship(back_populates="pedidos")
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[StatusPedido] = mapped_column(
        SQLEnum(StatusPedido), default=StatusPedido.PENDENTE, nullable=False
    )
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    itens: Mapped[list["ItemPedido"]] = relationship(back_populates="pedido")


class ItemPedido(Base):
    __tablename__ = "itens_pedidos"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantidade: Mapped[int] = mapped_column(nullable=False)
    preco_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    pedidos_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"), nullable=False)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produto.id"), nullable=False)

    pedido: Mapped["Pedido"] = relationship(back_populates="itens")
    produto: Mapped["Produto"] = relationship(back_populates="itens_pedidos")