from flask import Blueprint, request, render_template, redirect, url_for, flash
from sqlalchemy.orm import Session
from datetime import datetime
from models.base import SessionLocal
from models.testresults import TestResults
from models.accounts import Accounts

test_bp = Blueprint("test", __name__)

STAGES = ["喜", "怒", "哀", "樂"]

@test_bp.route("/test/<int:account_id>/<int:stage_index>", methods=["GET", "POST"])
def test_stage(account_id, stage_index):
    db: Session = SessionLocal()
    account = db.query(Accounts).filter_by(id=account_id).first()

    if not account:
        flash("帳號不存在")
        return redirect(url_for("auth.login"))

    stage = STAGES[stage_index]

    if request.method == "POST":
        child_choice = request.form["child_choice"]
        system_result = "O" if child_choice == stage else "X"

        result = TestResults(
            account_id=account.id,
            stage=stage,
            child_choice=child_choice,
            system_result=system_result,
            test_datetime=datetime.now()
        )
        db.add(result)
        db.commit()

        if stage_index + 1 < len(STAGES):
            return redirect(url_for("test.test_stage", account_id=account.id, stage_index=stage_index + 1))
        else:
            return redirect(url_for("test.results", account_id=account.id))

    return render_template("test.html", stage=stage, stage_index=stage_index)

@test_bp.route("/results/<int:account_id>")
def results(account_id):
    db: Session = SessionLocal()
    results = db.query(TestResults).filter_by(account_id=account_id).all()

    correct_count = sum(1 for r in results if r.system_result == "O")
    total = len(results)
    accuracy = (correct_count / total * 100) if total > 0 else 0

    return render_template("results.html", results=results, accuracy=accuracy)

@test_bp.route("/choose_type/<int:account_id>", methods=["GET", "POST"])
def choose_type(account_id):
    db: Session = SessionLocal()
    types = db.query(ExpressionTypes).all()
    if request.method == "POST":
        type_id = request.form["type_id"]
        return redirect(url_for("test.test_stage", account_id=account_id, stage_index=0, type_id=type_id))
    return render_template("choose_type.html", types=types)

@test_bp.route("/test/<int:account_id>/<int:stage_index>/<int:type_id>", methods=["GET", "POST"])
def test_stage_with_type(account_id, stage_index, type_id):
    db: Session = SessionLocal()
    stage = STAGES[stage_index]
    image = db.query(ExpressionImages).filter_by(type_id=type_id, stage=stage).first()

    if request.method == "POST":
        child_choice = request.form["child_choice"]
        system_result = "O" if child_choice == stage else "X"
        result = TestResults(account_id=account_id, stage=stage, child_choice=child_choice,
                             system_result=system_result, test_datetime=datetime.now())
        db.add(result)
        db.commit()
        if stage_index + 1 < len(STAGES):
            return redirect(url_for("test.test_stage", account_id=account_id, stage_index=stage_index+1, type_id=type_id))
        else:
            return redirect(url_for("test.results", account_id=account_id))
    return render_template("test.html", stage=stage, image=image)