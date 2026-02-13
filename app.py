from flask import Flask, render_template, redirect, url_for, request, session, flash
from routes.auth import auth_bp
from routes.test import test_bp
from routes.admin import admin_bp
from models.base import engine, SessionLocal
from models.expressionimages import ExpressionImages
from models.expressiontypes import ExpressionTypes
from datetime import datetime
from models.testresults import TestResults
import random

app = Flask(__name__)
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

    # 判斷系統正確答案
    system_result = "O" if child_choice == stage else "X"

    # ✅ 寫入 DB
    db = SessionLocal()
    account_id = session.get("user_id")
    test_result = TestResults(
        account_id=account_id,
        stage=stage,
        child_choice=child_choice,
        system_result=system_result,
        test_datetime=datetime.now()
    )
    db.add(test_result)
    db.commit()

    # 更新完成關卡
    completed = session.get("completed_stages", [])
    if stage not in completed:
        completed.append(stage)
    session["completed_stages"] = completed

    return redirect(url_for("play_stage"))


if __name__ == "__main__":
    app.run(debug=True)