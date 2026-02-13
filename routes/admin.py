from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from sqlalchemy.orm import Session
from models.base import SessionLocal
from models.expressiontypes import ExpressionTypes
from models.expressionimages import ExpressionImages
from models.testresults import TestResults
from models.accounts import Accounts
from collections import defaultdict

import os

from werkzeug.utils import secure_filename


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form["password"]
        if password == "978":
            session["is_admin"] = True
            return render_template("admin_login_success.html")
        else:
            flash("密碼錯誤")
            return redirect(url_for("admin.admin_login"))
    return render_template("admin_login.html")

@admin_bp.route("/")
def admin_index():
    if not session.get("is_admin"):
        flash("請先登入管理者")
        return redirect(url_for("admin.admin_login"))
    return render_template("admin_index.html")

@admin_bp.route("/add_type", methods=["GET", "POST"])
def add_type():
    if not session.get("is_admin"):
        flash("請先登入管理者")
        return redirect(url_for("admin.admin_login"))

    if request.method == "POST":
        type_name = request.form["type_name"]
        db: Session = SessionLocal()
        new_type = ExpressionTypes(type_name=type_name)
        db.add(new_type)
        db.commit()
        flash("新增類型成功")
        # ✅ 新增完成後導回後台首頁
        return redirect(url_for("admin.admin_index"))
    return render_template("add_type.html")


@admin_bp.route("/logout")
def admin_logout():
    session.pop("is_admin", None)
    flash("已登出管理者")
    return redirect(url_for("admin.admin_login"))



UPLOAD_FOLDER = os.path.join("static", "img")  # 建議放在 static/img
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route("/add_image", methods=["GET", "POST"])
def add_image():
    if not session.get("is_admin"):
        flash("請先登入管理者")
        return redirect(url_for("admin.admin_login"))

    db: Session = SessionLocal()
    types = db.query(ExpressionTypes).all()

    if request.method == "POST":
        type_id = request.form["type_id"]
        stage = request.form["stage"]

        # 檢查是否已存在同類型+表情
        existing = db.query(ExpressionImages).filter_by(type_id=type_id, stage=stage).first()
        if existing:
            # ✅ 不直接跳轉，先顯示提示訊息
            flash(f"該類型的表情『{stage}』已存在，請確認是否要編輯。")
            return render_template("add_image.html", types=types, existing_image=existing)

        file = request.files.get("image_file")
        if file and allowed_file(file.filename):
            filename = f"{type_id}_{stage}.png"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(filepath)

            new_image = ExpressionImages(
                type_id=type_id,
                stage=stage,
                image_path=f"img/{filename}"
            )
            db.add(new_image)
            db.commit()
            flash("新增圖片成功")
            return redirect(url_for("admin.admin_index"))
        else:
            flash("檔案格式不支援")

    return render_template("add_image.html", types=types)

@admin_bp.route("/images")
def image_list():
    if not session.get("is_admin"):
        flash("請先登入管理者")
        return redirect(url_for("admin.admin_login"))

    db: Session = SessionLocal()
    images = db.query(ExpressionImages).all()
    return render_template("image_list.html", images=images)

@admin_bp.route("/delete_image/<int:image_id>", methods=["POST"])
def delete_image(image_id):
    if not session.get("is_admin"):
        flash("請先登入管理者")
        return redirect(url_for("admin.admin_login"))

    db: Session = SessionLocal()
    image = db.query(ExpressionImages).filter_by(id=image_id).first()
    if image:
        # 刪除實際檔案
        filepath = os.path.join("static", image.image_path)
        if os.path.exists(filepath):
            os.remove(filepath)

        # 刪除資料庫紀錄
        db.delete(image)
        db.commit()
        flash("圖片已刪除")
    else:
        flash("找不到圖片")

    return redirect(url_for("admin.image_list"))

@admin_bp.route("/edit_image/<int:image_id>", methods=["GET", "POST"])
def edit_image(image_id):
    if not session.get("is_admin"):
        flash("請先登入管理者")
        return redirect(url_for("admin.admin_login"))

    db: Session = SessionLocal()
    image = db.query(ExpressionImages).filter_by(id=image_id).first()

    if not image:
        flash("找不到圖片")
        return redirect(url_for("admin.image_list"))

    if request.method == "POST":
        stage = request.form["stage"]
        file = request.files.get("image_file")

        # 更新表情階段
        image.stage = stage

        # 如果有重新上傳圖片
        if file and allowed_file(file.filename):
            filename = f"{image.type_id}_{stage}.png"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(filepath)
            image.image_path = f"img/{filename}"

        db.commit()
        flash("圖片已更新")
        return redirect(url_for("admin.image_list"))

    return render_template("edit_image.html", image=image)




@admin_bp.route("/results", methods=["GET", "POST"])
def view_results():
    db = SessionLocal()
    accounts = db.query(Accounts).all()
    grouped_results = []  # 每次測驗的分組結果

    if request.method == "POST":
        child_name = request.form["child_name"]
        account = db.query(Accounts).filter_by(child_name=child_name).first()
        if account:
            results = db.query(TestResults).filter_by(account_id=account.id).order_by(TestResults.test_datetime).all()

            # 依照每四筆為一組分批次
            batch = []
            for r in results:
                batch.append(r)
                if len(batch) == 4:  # 一次測驗完成
                    total = len(batch)
                    correct = sum(1 for x in batch if x.system_result == "O")
                    accuracy = round((correct / total) * 100, 2)
                    grouped_results.append({"records": batch, "accuracy": accuracy})
                    batch = []  # 清空，準備下一批

    return render_template("admin_results.html", accounts=accounts, grouped_results=grouped_results)