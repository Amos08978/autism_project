from models.base import SessionLocal
from models.expressionmapping import ExpressionMapping

db = SessionLocal()

default_mappings = [
    {"source_emotion": "happy", "mapped_stage": "喜"},
    {"source_emotion": "angry", "mapped_stage": "怒"},
    {"source_emotion": "sad", "mapped_stage": "哀"},
    {"source_emotion": "surprise", "mapped_stage": "樂"},
    {"source_emotion": "neutral", "mapped_stage": "樂"},
]

for m in default_mappings:
    exists = db.query(ExpressionMapping).filter_by(source_emotion=m["source_emotion"]).first()
    if not exists:
        db.add(ExpressionMapping(**m))

db.commit()
print("✅ 預設映射初始化完成")