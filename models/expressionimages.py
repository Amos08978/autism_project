from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class ExpressionImages(Base):
    __tablename__ = "expression_images"
    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("expression_types.id"), nullable=False)
    stage = Column(String(20), nullable=False)   # 喜、怒、哀、樂
    image_path = Column(String(200), nullable=False)  # static/img/... 路徑

    type = relationship("ExpressionTypes")