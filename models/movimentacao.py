from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    tipo = Column(String, nullable=False)
    data = Column(Date, nullable=False)

    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    categoria = relationship("Categoria", back_populates="movimentacoes")