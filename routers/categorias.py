from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import conectar
from models.categorias import Categoria
from schemas.categorias import CategoriaCreate, CategoriaResponse


router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)


# Cadastrar categoria
@router.post("/", response_model=CategoriaResponse, status_code=201)
def criar_categoria(
    categoria: CategoriaCreate,
    db: Session = Depends(conectar)
):
    nova_categoria = Categoria(**categoria.model_dump())

    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)

    return nova_categoria


# Listar categorias
@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(db: Session = Depends(conectar)):
    categorias = db.query(Categoria).order_by(Categoria.id).all()

    return categorias