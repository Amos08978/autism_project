from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base   # ← 這行一定要有

class ExpressionImages(Base):
    __tablename__ = "expression_images"
    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("expression_types.id"), nullable=False)
    stage = Column(String(20), nullable=False)
    image_path = Column(String(200), nullable=False)

    type = relationship("ExpressionTypes", back_populates="images")
    results = relationship("TestResults", back_populates="image", cascade="all, delete-orphan")