from enum import Enum 
from sqlalchemy import Enum as SQLEnum
from decimal import Decimal
from sqlalchemy import create_engine, String, Numeric, ForeignKey,  DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database import Base
from datetime import datetime


class produtos(Base):
    __tablename__="produto"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    categoria: Mapped[str] = mapped_column(String(100))
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    estoque: Mapped[int] = mapped_column(nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    itens_pedidos: Mapped[list["itenspedidos"]] = relationship(back_populates="produto")

class usuario(Base):
    __tablename__="usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String(20), default="cliente", nullable=False)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str | None] = mapped_column(unique=True)
    senha: Mapped[str] = mapped_column(String(100))
    data_criacao: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    pedidos: Mapped[list["pedido"]] = relationship(back_populates="usuario")

class statuspedido(str, Enum):
    PENDENTE = "pendente"
    PAGO = "pago"
    ENVIADO = "enviado"
    CANCELADO = "cancelado"

class pedido(Base):
    __tablename__="pedidos"
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    usuario: Mapped["usuario"] = relationship(back_populates="pedidos")
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[statuspedido] = mapped_column(SQLEnum(statuspedido), default=statuspedido.PENDENTE, nullable=False) 
    data_criacao: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    itens: Mapped[list["itenspedidos"]] = relationship(back_populates="pedido")

class itenspedidos(Base):
    __tablename__="itens_pedidos"
    id: Mapped[int] = mapped_column(primary_key=True)
    quantidade: Mapped[int] = mapped_column(nullable=False)
    preco_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    pedidos_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"), nullable=False) 
    produto_id: Mapped[int] = mapped_column(ForeignKey("produto.id"), nullable=False)

    pedido: Mapped["pedido"] = relationship(back_populates="itens")
    produto: Mapped["produtos"] = relationship(back_populates="itens_pedidos")



