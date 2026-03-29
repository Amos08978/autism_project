from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from models.base import Base

class ExpressionImages(Base):
    __tablename__ = "expression_images"
    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("expression_types.id"), nullable=False)
    stage = Column(String(20), nullable=False)
    image_path = Column(String(200), nullable=False)
    audio_path = Column(String(200), nullable=True)   # ✅ 新增音檔欄位

    __table_args__ = (UniqueConstraint("type_id", "stage", name="uix_type_stage"),)

    type = relationship("ExpressionTypes", back_populates="images")
    results = relationship("TestResults", back_populates="image", cascade="all, delete-orphan")