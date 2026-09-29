from typing import Optional

from pydantic import BaseModel


class CriarProduto(BaseModel):
    name: str
    categoria: str
    preco: float
    estoque: int


class AtualizarProduto(BaseModel):
    name: Optional[str] = None
    categoria: Optional[str] = None
    preco: Optional[float] = None
    estoque: Optional[int] = None