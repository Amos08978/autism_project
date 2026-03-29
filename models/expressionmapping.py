from sqlalchemy import Column, Integer, String
from models.base import Base

class ExpressionMapping(Base):
    __tablename__ = "expression_mapping"
    id = Column(Integer, primary_key=True)
    source_emotion = Column(String)   # AI 辨識到的表情
    mapped_stage = Column(String)     # 對應的遊戲關卡