from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from models.base import Base

class Accounts(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    parent_name = Column(String(100), nullable=False)
    child_name = Column(String(100), nullable=False)
    child_age = Column(Integer, nullable=False)
    phone = Column(String(20))
    address = Column(String(200))
    email = Column(String(100))
    line = Column(String(100))
    privacy_signed_at = Column(TIMESTAMP, default=None)  # ✅ 新增欄位

    # 關聯到 TestResults
    results = relationship("TestResults", back_populates="account", cascade="all, delete-orphan")