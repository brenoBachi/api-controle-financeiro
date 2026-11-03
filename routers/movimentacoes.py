from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import conectar
from models.movimentacao import Movimentacao
from schemas.movimentacao import MovimentacaoCreate, MovimentacaoResponse


router = APIRouter(
    prefix="/movimentacoes",
    tags=["Movimentações"]
)

# Criar Movimentação
@router.post(
    "/",
    response_model=MovimentacaoResponse,
    status_code=201
)
def criar_movimentacao(
    movimentacao: MovimentacaoCreate,
    db: Session = Depends(conectar)
):
    nova_movimentacao = Movimentacao(**movimentacao.model_dump())

    db.add(nova_movimentacao)
    db.commit()
    db.refresh(nova_movimentacao)

    return nova_movimentacao

# Listar Movimentações
@router.get("/", response_model=list[MovimentacaoResponse])
def listar_movimentacoes(db: Session = Depends(conectar)):
    movimentacoes = db.query(Movimentacao).all()
    return movimentacoes

# Buscar Movimentação por ID
@router.get("/{movimentacao_id}", response_model=MovimentacaoResponse)
def buscar_movimentacao(
    movimentacao_id: int,
    db: Session = Depends(conectar)
):
    movimentacao = db.query(Movimentacao).filter(
        Movimentacao.id == movimentacao_id
    ).first()

    if movimentacao is None:
        raise HTTPException(
            status_code=404,
            detail="Movimentação não encontrada"
        )

    return movimentacao

# Atualizar Movimentação
@router.put("/{movimentacao_id}", response_model=MovimentacaoResponse)
def atualizar_movimentacao(
    movimentacao_id: int,
    dados: MovimentacaoCreate,
    db: Session = Depends(conectar)
):
    movimentacao = db.query(Movimentacao).filter(
        Movimentacao.id == movimentacao_id
    ).first()

    if movimentacao is None:
        raise HTTPException(
            status_code=404,
            detail="Movimentação não encontrada"
        )

    movimentacao.descricao = dados.descricao
    movimentacao.valor = dados.valor
    movimentacao.tipo = dados.tipo
    movimentacao.data = dados.data

    db.commit()
    db.refresh(movimentacao)

    return movimentacao

# Excluir Movimentação
@router.delete("/{movimentacao_id}", status_code=204)
def excluir_movimentacao(
    movimentacao_id: int,
    db: Session = Depends(conectar)
):
    movimentacao = db.query(Movimentacao).filter(
        Movimentacao.id == movimentacao_id
    ).first()

    if movimentacao is None:
        raise HTTPException(
            status_code=404,
            detail="Movimentação não encontrada"
        )

    db.delete(movimentacao)
    db.commit()