from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)

    movimentacoes = relationship("Movimentacao", back_populates="categoria")