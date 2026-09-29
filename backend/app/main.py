from fastapi import FastAPI

from app.routers import auth, pedidos, produtos

app = FastAPI()
app.include_router(auth.router)
app.include_router(produtos.router)
app.include_router(pedidos.router)