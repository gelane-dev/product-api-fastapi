from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String(20), default="cliente", nullable=False)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str | None] = mapped_column(unique=True)
    senha: Mapped[str] = mapped_column(String(100))
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    pedidos: Mapped[list["Pedido"]] = relationship(back_populates="usuario")