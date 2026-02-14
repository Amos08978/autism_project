from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class TestResults(Base):
    __tablename__ = "testresults"   # 與 DB 表名一致
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    image_id = Column(Integer, ForeignKey("expression_images.id"), nullable=False)  # 新增外鍵
    stage = Column(String(20), nullable=False)
    child_choice = Column(String(20), nullable=False)
    system_result = Column(String(5), nullable=False)
    test_datetime = Column(TIMESTAMP, default=datetime.now)
    batch_id = Column(String(50))
    # 關聯到 Accounts
    account = relationship("Accounts", back_populates="results")

    # 關聯到 ExpressionImages
    image = relationship("ExpressionImages", back_populates="results")