from flask import Flask, render_template, redirect, url_for, request, session, flash
from routes.auth import auth_bp
from routes.test import test_bp
from routes.admin import admin_bp
from models.base import engine, SessionLocal
from models.expressionimages import ExpressionImages
from models.expressiontypes import ExpressionTypes
from datetime import datetime
from models.testresults import TestResults
from flask import jsonify
from models.capturesettings import CaptureSettings
from hsemotion.facial_emotions import HSEmotionRecognizer
from models.testrecord import TestRecord
from models.expressionmapping import ExpressionMapping


import random,uuid,os,time,base64
from io import BytesIO
from PIL import Image
import numpy as np

import timm
import torch.serialization
torch.serialization.add_safe_globals([timm.models.efficientnet.EfficientNet])

app = Flask(__name__)

fer = HSEmotionRecognizer(model_name='enet_b0_8_best_afew', device='cpu')


app.secret_key = "secret_key"

app.register_blueprint(auth_bp)
app.register_blueprint(test_bp)
app.register_blueprint(admin_bp)


@app.route("/")
def index():
    return render_template("index.html")   # 登入頁


@app.route("/game_home")
def game_home():
    if not session.get("user_id"):
        flash("請先登入")
        return redirect(url_for("auth.login"))

    db = SessionLocal()
    types = db.query(ExpressionTypes).all()
    return render_template("game_home.html", types=types)


@app.route("/select_type", methods=["GET", "POST"])
def select_type():
    db = SessionLocal()
    if request.method == "POST":
        type_id = request.form["type_id"]
        session["selected_type"] = type_id
        session["completed_stages"] = []
        session["batch_id"] = str(uuid.uuid4())
        return redirect(url_for("play_stage"))
    types = db.query(ExpressionTypes).all()
    return render_template("select_type.html", types=types)


@app.route("/play_stage")
def play_stage():
    type_id = session.get("selected_type")
    completed = session.get("completed_stages", [])

    all_stages = ["喜", "怒", "哀", "樂"]
    remaining = [s for s in all_stages if s not in completed]

    if not remaining:
        return render_template("game_complete.html")

    stage = random.choice(remaining)
    db = SessionLocal()
    image = db.query(ExpressionImages).filter_by(type_id=type_id, stage=stage).first()

    return render_template("play_stage.html", stage=stage, image=image)




@app.route("/finish_stage/<stage>", methods=["POST"])
def finish_stage(stage):
    child_choice = request.form["child_choice"]
    image_id = request.form.get("image_id")
    if not image_id:
        flash("尚未設定圖片，無法寫入測試結果")
        return redirect(url_for("play_stage"))

    system_result = "O" if child_choice == stage else "X"

    db = SessionLocal()
    account_id = session.get("user_id")
    batch_id = session.get("batch_id")  # ✅ 取出批次 ID

    test_result = TestResults(
        account_id=account_id,
        image_id=int(image_id),
        stage=stage,
        child_choice=child_choice,
        system_result=system_result,
        test_datetime=datetime.now(),
        batch_id=batch_id  # ✅ 存入 DB
    )
    db.add(test_result)
    db.commit()

    completed = session.get("completed_stages", [])
    if stage not in completed:
        completed.append(stage)
    session["completed_stages"] = completed

    return redirect(url_for("learn_stage", stage=stage))


#學一學

@app.route("/learn_stage/<stage>")
def learn_stage(stage):
    type_id = session.get("selected_type")
    db = SessionLocal()
    image = db.query(ExpressionImages).filter_by(type_id=type_id, stage=stage).first()
    settings = db.query(CaptureSettings).first()
    return render_template("learn_stage.html", stage=stage, image=image,
                           interval=settings.interval, times=settings.times)





@app.route("/check_expression/<stage>", methods=["POST"])
def check_expression(stage):
    data = request.get_json()
    img_data = data["image"].split(",")[1]
    img_bytes = base64.b64decode(img_data)
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    frame = np.array(img)

    # 儲存截圖
    save_dir = "static/captured_images"
    os.makedirs(save_dir, exist_ok=True)
    filename = f"{stage}_{int(time.time())}.png"
    filepath = os.path.join(save_dir, filename)
    img.save(filepath)

    # 模型預測
    emotion, score = fer.predict_emotions(frame)

    db = SessionLocal()
    rule = db.query(ExpressionMapping).filter_by(source_emotion=emotion).first()
    mapped_emotion = rule.mapped_stage if rule else "未知"
    result = "O" if mapped_emotion == stage else "X"

    record = TestRecord(
        batch_id=session.get("batch_id"),
        account_id=session.get("user_id"),
        stage=stage,
        child_choice=None,
        system_result=result,
        ai_emotion=emotion,
        image_file=filename,
        test_datetime=datetime.now()
    )
    db.add(record)
    db.commit()

    return jsonify({
        "result": result,
        "emotion": emotion,
        "file": filename,
        "success": True if result == "O" else False
    })


if __name__ == "__main__":
    app.run(debug=True)