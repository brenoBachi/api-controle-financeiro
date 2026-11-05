from fastapi import FastAPI
from database import engine, Base
from models.movimentacao import Movimentacao
from routers.movimentacoes import router as movimentacoes_router
from models.categorias import Categoria
from routers.categorias import router as categorias_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Controle Financeiro")

app.include_router(movimentacoes_router)
app.include_router(categorias_router)

@app.get("/")
def inicio():
    return {"mensagem": "API de Controle Financeiro funcionando!"}