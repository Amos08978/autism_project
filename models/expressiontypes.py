from sqlalchemy import Column, Integer, String
from models.base import Base

class ExpressionTypes(Base):
    __tablename__ = "expression_types"
    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String(50), nullable=False, unique=True)  # 例如: 卡通、寫實、動物