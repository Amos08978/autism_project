from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from sqlalchemy.orm import Session
from models.base import SessionLocal
from models.expressiontypes import ExpressionTypes
from models.expressionimages import ExpressionImages
from models.expressionmapping import ExpressionMapping
from models.testresults import TestResults
from models.accounts import Accounts
from collections import defaultdict
from sqlalchemy.orm import joinedload
from datetime import datetime
from models.capturesettings import CaptureSettings
from models.testrecord import TestRecord
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc



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
        type_id = int(request.form["type_id"])
        stage = request.form["stage"].strip()

        file = request.files.get("image_file")
        audio_file = request.files.get("audio_file")

        if file and allowed_file(file.filename):
            # 儲存圖片
            filename = f"{type_id}_{stage}.png"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(filepath)

            # 儲存音檔（可選）
            audio_path = None
            if audio_file and audio_file.filename != "":
                audio_filename = f"{type_id}_{stage}.mp3"
                audio_folder = os.path.join("static", "audio")
                os.makedirs(audio_folder, exist_ok=True)
                audio_file.save(os.path.join(audio_folder, audio_filename))
                audio_path = f"audio/{audio_filename}"

            new_image = ExpressionImages(
                type_id=type_id,
                stage=stage,
                image_path=f"img/{filename}",
                audio_path=audio_path
            )
            db.add(new_image)
            try:
                db.commit()
                flash("新增圖片成功")
                return redirect(url_for("admin.image_list"))
            except IntegrityError:
                db.rollback()
                flash(f"該類型的表情『{stage}』已存在，請改用編輯功能。")
                return redirect(url_for("admin.image_list"))
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

    if request.method == "POST":
        image.stage = request.form["stage"].strip()
        image.type_id = int(request.form["type_id"])

        file = request.files.get("image_file")
        audio_file = request.files.get("audio_file")

        # 更新圖片（可選）
        if file and allowed_file(file.filename):
            filename = f"{image.type_id}_{image.stage}.png"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(filepath)
            image.image_path = f"img/{filename}"

        # 更新音檔（可選）
        if audio_file and audio_file.filename != "":
            audio_filename = f"{image.type_id}_{image.stage}.mp3"
            audio_folder = os.path.join("static", "audio")
            os.makedirs(audio_folder, exist_ok=True)
            audio_file.save(os.path.join(audio_folder, audio_filename))
            image.audio_path = f"audio/{audio_filename}"

        try:
            db.commit()
            flash("更新成功")
            return redirect(url_for("admin.image_list"))
        except IntegrityError:
            db.rollback()
            flash(f"該類型的表情『{image.stage}』已存在，請改用其他組合。")
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
            # 小朋友選擇紀錄 (TestResults) → 最新在最上面
            results = (
                db.query(TestResults)
                .options(joinedload(TestResults.image).joinedload(ExpressionImages.type))
                .filter_by(account_id=account.id)
                .order_by(desc(TestResults.test_datetime))
                .all()
            )

            # AI 判斷紀錄 (TestRecord) → 最新在最上面
            records_ai = (
                db.query(TestRecord)
                .filter_by(account_id=account.id)
                .order_by(desc(TestRecord.test_datetime))
                .all()
            )

            # 用 batch_id 合併
            batches = {}
            for r in results:
                batch_id = r.batch_id or "未知批次"
                if batch_id not in batches:
                    batches[batch_id] = {"results": [], "records_ai": []}
                batches[batch_id]["results"].append(r)
                total_records += 1

                if r.image and r.image.type:
                    type_name = r.image.type.type_name
                    type_counts[type_name] = type_counts.get(type_name, 0) + 1

            for rec in records_ai:
                batch_id = rec.batch_id or "未知批次"
                if batch_id not in batches:
                    batches[batch_id] = {"results": [], "records_ai": []}
                batches[batch_id]["records_ai"].append(rec)

            # 整理成 grouped_results，依照時間排序
            sorted_batches = sorted(
                batches.items(),
                key=lambda x: x[1]["results"][0].test_datetime if x[1]["results"] else None,
                reverse=True  # 最新在最上面
            )

            total_batches = len(sorted_batches)
            for idx, (batch_id, batch) in enumerate(sorted_batches, start=1):
                # 計算編號：最新一筆 = 第 total_batches 次
                test_number = total_batches - idx + 1

                type_name = (
                    batch["results"][0].image.type.type_name
                    if batch["results"] and batch["results"][0].image and batch["results"][0].image.type
                    else "未知"
                )
                start_time = batch["results"][0].test_datetime if batch["results"] else None

                if len(batch["results"]) == 4:
                    correct = sum(1 for x in batch["results"] if x.system_result == "O")
                    accuracy = round((correct / 4) * 100, 2)
                    grouped_results.append({
                        "results": batch["results"],
                        "records_ai": batch["records_ai"],
                        "accuracy": accuracy,
                        "test_number": test_number,
                        "incomplete": False,
                        "type_name": type_name,
                        "batch_id": batch_id,
                        "start_time": start_time
                    })
                else:
                    grouped_results.append({
                        "results": batch["results"],
                        "records_ai": batch["records_ai"],
                        "accuracy": None,
                        "test_number": test_number,
                        "incomplete": True,
                        "type_name": type_name,
                        "batch_id": batch_id,
                        "start_time": start_time
                    })

    # 統計各類型比例
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





@admin_bp.route("/mapping_list")
def mapping_list():
    db = SessionLocal()
    mappings = db.query(ExpressionMapping).all()
    return render_template("admin_mapping.html", mappings=mappings)

@admin_bp.route("/mapping_add", methods=["POST"])
def mapping_add():
    source_emotion = request.form["source_emotion"]
    mapped_stage = request.form["mapped_stage"]

    db = SessionLocal()
    new_map = ExpressionMapping(source_emotion=source_emotion, mapped_stage=mapped_stage)
    db.add(new_map)
    db.commit()
    flash("新增映射成功")
    return redirect(url_for("admin.mapping_list"))

@admin_bp.route("/mapping_edit/<int:id>", methods=["POST"])
def mapping_edit(id):
    mapped_stage = request.form["mapped_stage"]
    db = SessionLocal()
    mapping = db.query(ExpressionMapping).get(id)
    if mapping:
        mapping.mapped_stage = mapped_stage
        db.commit()
        flash("更新成功")
    return redirect(url_for("admin.mapping_list"))

@admin_bp.route("/mapping_delete/<int:id>", methods=["POST"])
def mapping_delete(id):
    db = SessionLocal()
    mapping = db.query(ExpressionMapping).get(id)
    if mapping:
        db.delete(mapping)
        db.commit()
        flash("刪除成功")
    return redirect(url_for("admin.mapping_list"))

@admin_bp.route("/update_capture_settings", methods=["POST"])
def update_capture_settings():
    interval = int(request.form["interval"])
    times = int(request.form["times"])
    db = SessionLocal()
    settings = db.query(CaptureSettings).first()
    if not settings:
        settings = CaptureSettings(interval=interval, times=times)
        db.add(settings)
    else:
        settings.interval = interval
        settings.times = times
    db.commit()
    flash("拍照設定已更新", "success")
    return redirect(url_for("admin.mapping"))

@admin_bp.route("/mapping")
def mapping():
    db = SessionLocal()
    mappings = db.query(ExpressionMapping).all()
    settings = db.query(CaptureSettings).first()
    return render_template("admin_mapping.html",
                           mappings=mappings,
                           interval=settings.interval if settings else 5,
                           times=settings.times if settings else 3)

@admin_bp.route("/result_override/<int:id>", methods=["POST"])
def result_override(id):
    new_result = request.form["final_result"]
    db = SessionLocal()
    record = db.query(TestRecord).filter_by(id=id).first()
    if record:
        record.manual_override = True
        record.final_result = new_result
        db.commit()
        flash("人工覆核已更新", "success")
    return redirect(url_for("admin.view_results"))  # 或者跳回 admin.results