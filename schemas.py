from pydantic import BaseModel, EmailStr, Field
from typing import Optional, list
from datetime import datetime

class criarproduto(BaseModel):
    name: str
    categoria: str
    preco: float
    estoque: int



class atualizarproduto(BaseModel):
    name: Optional[str]=None
    categoria: Optional[str]=None
    preco: Optional[float]=None
    estoque: Optional[int]=None
       
class criarusuarios(BaseModel):
    name: str = Field(min_lenght=3, max_lenght=100)
    email: EmailStr
    senha: str = Field(min_lenght=6)

class itempedido(BaseModel):
    produto_id: int
    quantidade: int

class criarpedido(BaseModel):
    itens: list[itempedido]