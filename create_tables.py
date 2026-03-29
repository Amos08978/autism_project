from models.base import Base, engine
from models.accounts import Accounts   # ✅ 加上這行
from models.testrecord import TestRecord
from models.expressionimages import ExpressionImages
from models.expressionmapping import ExpressionMapping
from models.expressiontypes import ExpressionTypes
from models.capturesettings import CaptureSettings
from models.testresults import TestResults

def create_all_tables():
    Base.metadata.create_all(bind=engine)
    print("所有資料表已建立完成")

if __name__ == "__main__":
    create_all_tables()