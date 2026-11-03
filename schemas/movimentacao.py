from pydantic import BaseModel, Field
from datetime import date
from typing import Literal

class MovimentacaoBase(BaseModel):
    descricao: str
    valor: float = Field(gt=0)
    tipo: Literal["receita", "despesa"]
    data: date

class MovimentacaoCreate(MovimentacaoBase):
    pass

class MovimentacaoResponse(MovimentacaoBase):
    id: int

    class Config:
        from_attributes = True

class MovimentacaoPaginada(BaseModel):
    total: int
    limit: int
    offset: int
    total_paginas: int
    movimentacoes: list[MovimentacaoResponse]