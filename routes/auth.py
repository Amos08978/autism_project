from flask import Blueprint, request, render_template, redirect, url_for, flash
from sqlalchemy.orm import Session
from datetime import datetime
from models.base import SessionLocal
from models.accounts import Accounts
from models.loginlog import LoginLog
from flask import session

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        parent_name = request.form["parent_name"]
        child_name = request.form["child_name"]

        db: Session = SessionLocal()
        account = db.query(Accounts).filter_by(parent_name=parent_name, child_name=child_name).first()

        if account:
            # 登入成功 → 寫入 LoginLog
            log = LoginLog(
                account_id=account.id,
                login_result="success",
                reason="登入成功",
                login_datetime=datetime.now()
            )
            db.add(log)
            db.commit()

            # ✅ 存入 session
            session["user_id"] = account.id
            session["child_name"] = account.child_name

            flash("登入成功！")
            return redirect(url_for("game_home"))
        else:
            log = LoginLog(
                account_id=None,
                login_result="fail",
                reason="帳號不存在",
                login_datetime=datetime.now()
            )
            db.add(log)
            db.commit()
            flash("無此帳號，請先註冊")
            return redirect(url_for("auth.register"))

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        parent_name = request.form["parent_name"]
        child_name = request.form["child_name"]
        child_age = request.form["child_age"]
        phone = request.form["phone"]
        address = request.form["address"]
        email = request.form["email"]
        line = request.form["line"]

        db: Session = SessionLocal()
        account = db.query(Accounts).filter_by(parent_name=parent_name, child_name=child_name).first()

        if account:
            flash("帳號已存在，無法註冊")
        else:
            new_account = Accounts(
                parent_name=parent_name,
                child_name=child_name,
                child_age=int(child_age),
                phone=phone,
                address=address,
                email=email,
                line=line
            )
            db.add(new_account)
            db.commit()
            flash("註冊成功！請重新登入")
            return redirect(url_for("auth.login"))

    return render_template("register.html")