from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from models.base import Base
from datetime import datetime

class TestRecord(Base):
    __tablename__ = "test_records"
    id = Column(Integer, primary_key=True)
    batch_id = Column(String, index=True)       # 批次 ID
    account_id = Column(Integer, ForeignKey("accounts.id"))  # ✅ 新增欄位
    test_datetime = Column(DateTime, default=datetime.now)
    stage = Column(String)
    child_choice = Column(String)
    system_result = Column(String)              # O / X
    ai_emotion = Column(String)                 # AI 判斷的表情
    image_file = Column(String)                 # 截圖檔名
    manual_override = Column(Boolean, default=False)
    final_result = Column(String)