from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class ExpressionTypes(Base):
    __tablename__ = "expression_types"   # 與 DB 表名一致
    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String(50), nullable=False, unique=True)
    image_path = Column(String(200), nullable=True)  # 選單圖片

    # 反向關聯，對應 ExpressionImages.type
    images = relationship("ExpressionImages", back_populates="type", cascade="all, delete-orphan")