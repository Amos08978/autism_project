from sqlalchemy import Column, Integer
from models.base import Base

class CaptureSettings(Base):
    __tablename__ = "capture_settings"
    id = Column(Integer, primary_key=True)
    interval = Column(Integer, default=5)  # 每隔幾秒拍一次
    times = Column(Integer, default=3)     # 拍照次數