from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class LoginLog(Base):
    __tablename__ = "loginlog"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    login_result = Column(String(20), nullable=False)
    reason = Column(String(200))
    login_datetime = Column(TIMESTAMP, default=datetime.now)

    account = relationship("Accounts")