from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Produto(Base):
    __tablename__ = "produto"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    categoria: Mapped[str] = mapped_column(String(100))
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    estoque: Mapped[int] = mapped_column(nullable=False)
    imagem_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    itens_pedidos: Mapped[list["ItemPedido"]] = relationship(
        back_populates="produto"
    )