from pydantic import BaseModel
from typing import Optional
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
       
