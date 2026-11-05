from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import conectar
from models.movimentacao import Movimentacao
from schemas.movimentacao import (
    MovimentacaoCreate,
    MovimentacaoResponse,
    MovimentacaoPaginada
)

from typing import Literal
from datetime import date
from sqlalchemy import func

from models.categorias import Categoria


router = APIRouter(
    prefix="/movimentacoes",
    tags=["Movimentações"]
)

# Consultar Saldo
@router.get("/saldo")
def consultar_saldo(
    data_inicio: date | None = None,
    data_fim: date | None = None,
    db: Session = Depends(conectar)
):

    if data_inicio and data_fim and data_inicio > data_fim:
        raise HTTPException(
            status_code=400,
            detail="A data inicial não pode ser posterior à data final"
        )

    consulta_receitas = db.query(func.sum(Movimentacao.valor)).filter(
        Movimentacao.tipo == "receita"
    )

    consulta_despesas = db.query(func.sum(Movimentacao.valor)).filter(
        Movimentacao.tipo == "despesa"
    )

    if data_inicio:
        consulta_receitas = consulta_receitas.filter(
            Movimentacao.data >= data_inicio
        )
        consulta_despesas = consulta_despesas.filter(
            Movimentacao.data >= data_inicio
        )

    if data_fim:
        consulta_receitas = consulta_receitas.filter(
            Movimentacao.data <= data_fim
        )
        consulta_despesas = consulta_despesas.filter(
            Movimentacao.data <= data_fim
        )

    receitas = consulta_receitas.scalar() or 0
    despesas = consulta_despesas.scalar() or 0

    return {
        "total_receitas": receitas,
        "total_despesas": despesas,
        "saldo": receitas - despesas
    }

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
    categoria = db.query(Categoria).filter(
        Categoria.id == movimentacao.categoria_id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
    )

    nova_movimentacao = Movimentacao(**movimentacao.model_dump())

    db.add(nova_movimentacao)
    db.commit()
    db.refresh(nova_movimentacao)

    return nova_movimentacao

# Listar Movimentações
@router.get("/", response_model=MovimentacaoPaginada)
def listar_movimentacoes(
    tipo: Literal["receita", "despesa"] | None = None,
    data_inicio: date | None = None,
    data_fim: date | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(conectar)
):

    if data_inicio and data_fim and data_inicio > data_fim:
        raise HTTPException(
            status_code=400,
            detail="A data inicial não pode ser posterior à data final"
    )

    consulta = db.query(Movimentacao)

    if tipo:
        consulta = consulta.filter(Movimentacao.tipo == tipo)

    if data_inicio:
        consulta = consulta.filter(Movimentacao.data >= data_inicio)

    if data_fim:
        consulta = consulta.filter(Movimentacao.data <= data_fim)

    total = consulta.count()
    total_paginas = (total + limit - 1) // limit

    movimentacoes = consulta.order_by(
        Movimentacao.id
    ).offset(offset).limit(limit).all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "total_paginas": total_paginas,
        "movimentacoes": movimentacoes
    }

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

