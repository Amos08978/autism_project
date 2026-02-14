from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from sqlalchemy.orm import Session
from models.base import SessionLocal
from models.expressiontypes import ExpressionTypes
from models.expressionimages import ExpressionImages
from models.testresults import TestResults
from models.accounts import Accounts
from collections import defaultdict
from sqlalchemy.orm import joinedload
from datetime import datetime
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
        file = request.files.get("image_file")

        image_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(filepath)
            image_path = f"img/{filename}"

        db: Session = SessionLocal()
        new_type = ExpressionTypes(type_name=type_name, image_path=image_path)
        db.add(new_type)
        db.commit()
        flash("新增類型成功")
        return redirect(url_for("admin.type_list"))

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
    types = db.query(ExpressionTypes).all()

    if not image:
        flash("找不到圖片")
        return redirect(url_for("admin.image_list"))

    if request.method == "POST":
        image.type_id = request.form["type_id"]
        image.stage = request.form["stage"]
        file = request.files.get("image_file")

        if file and allowed_file(file.filename):
            filename = f"{image.type_id}_{image.stage}.png"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(filepath)
            image.image_path = f"img/{filename}"

        db.commit()
        flash("圖片已更新")
        return redirect(url_for("admin.image_list"))

    return render_template("edit_image.html", image=image, types=types)



@admin_bp.route("/results", methods=["GET", "POST"])
def view_results():
    db = SessionLocal()
    accounts = db.query(Accounts).all()
    grouped_results = []
    selected_child = None
    type_counts = {}
    total_records = 0

    if request.method == "POST":
        child_name = request.form["child_name"]
        selected_child = child_name
        account = db.query(Accounts).filter_by(child_name=child_name).first()
        if account:
            results = (
                db.query(TestResults)
                .options(joinedload(TestResults.image).joinedload(ExpressionImages.type))
                .filter_by(account_id=account.id)
                .order_by(TestResults.test_datetime)
                .all()
            )

            # ✅ 改成用 batch_id 分組
            batches = {}
            for r in results:
                batch_id = r.batch_id or "未知批次"
                if batch_id not in batches:
                    batches[batch_id] = []
                batches[batch_id].append(r)
                total_records += 1

                # 統計類型次數
                if r.image and r.image.type:
                    type_name = r.image.type.type_name
                    type_counts[type_name] = type_counts.get(type_name, 0) + 1

            test_number = 0
            for batch_id, batch in batches.items():
                test_number += 1
                type_name = batch[0].image.type.type_name if batch[0].image and batch[0].image.type else "未知"
                start_time = batch[0].test_datetime

                if len(batch) == 4:
                    correct = sum(1 for x in batch if x.system_result == "O")
                    accuracy = round((correct / 4) * 100, 2)
                    grouped_results.append({
                        "records": batch,
                        "accuracy": accuracy,
                        "test_number": test_number,
                        "incomplete": False,
                        "type_name": type_name,
                        "batch_id": batch_id,
                        "start_time": start_time
                    })
                else:
                    grouped_results.append({
                        "records": batch,
                        "accuracy": None,
                        "test_number": test_number,
                        "incomplete": True,
                        "type_name": type_name,
                        "batch_id": batch_id,
                        "start_time": start_time
                    })

    # 計算比例
    type_stats = []
    for type_name, count in type_counts.items():
        percentage = round((count / total_records) * 100, 2) if total_records > 0 else 0
        type_stats.append({"type_name": type_name, "count": count, "percentage": percentage})

    return render_template(
        "admin_results.html",
        accounts=accounts,
        grouped_results=grouped_results,
        selected_child=selected_child,
        type_stats=type_stats
    )




@admin_bp.route("/types")
def type_list():
    if not session.get("is_admin"):
        flash("請先登入管理者")
        return redirect(url_for("admin.admin_login"))

    db: Session = SessionLocal()
    types = db.query(ExpressionTypes).all()
    return render_template("type_list.html", types=types)

@admin_bp.route("/edit_type/<int:type_id>", methods=["GET", "POST"])
def edit_type(type_id):
    if not session.get("is_admin"):
        flash("請先登入管理者")
        return redirect(url_for("admin.admin_login"))

    db: Session = SessionLocal()
    type_obj = db.query(ExpressionTypes).filter_by(id=type_id).first()

    if not type_obj:
        flash("找不到類型")
        return redirect(url_for("admin.type_list"))

    if request.method == "POST":
        type_obj.type_name = request.form["type_name"]
        file = request.files.get("image_file")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(filepath)
            type_obj.image_path = f"img/{filename}"

        db.commit()
        flash("類型已更新")
        return redirect(url_for("admin.type_list"))

    return render_template("edit_type.html", type_obj=type_obj)


@admin_bp.route("/delete_type/<int:type_id>", methods=["POST"])
def delete_type(type_id):
    if not session.get("is_admin"):
        flash("請先登入管理者")
        return redirect(url_for("admin.admin_login"))

    db: Session = SessionLocal()
    type_obj = db.query(ExpressionTypes).filter_by(id=type_id).first()

    if type_obj:
        # 刪除選單圖片檔案
        if type_obj.image_path:
            filepath = os.path.join("static", type_obj.image_path)
            if os.path.exists(filepath):
                os.remove(filepath)

        db.delete(type_obj)
        db.commit()
        flash("類型已刪除")
    else:
        flash("找不到類型")

    return redirect(url_for("admin.type_list"))