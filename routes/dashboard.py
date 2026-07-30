from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from app import db

from models.transaction import Transaction
from models.savings_goal import SavingsGoal
from models.budget import Budget


dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/", methods=["GET"])
@jwt_required()
def get_dashboard():

    user_id = get_jwt_identity()

    income = (
        db.session.query(
            func.coalesce(func.sum(Transaction.amount), 0)
        )
        .filter(
            Transaction.user_id == user_id,
            Transaction.type == "credit"
        )
        .scalar()
    )

    expenses = (
        db.session.query(
            func.coalesce(func.sum(Transaction.amount), 0)
        )
        .filter(
            Transaction.user_id == user_id,
            Transaction.type == "debit"
        )
        .scalar()
    )

    net_worth = income - expenses

    budgets = Budget.query.filter_by(
        user_id=user_id
    ).all()

    return jsonify({
        "netWorth": net_worth,
        "monthlyIncome": income,
        "monthlyExpenses": expenses,
        "budgets": [
            budget.to_dict()
            for budget in budgets
        ]
    }), 200

@dashboard_bp.route("/weekly-spend", methods=["GET"])
@jwt_required()
def weekly_spend():

    user_id = get_jwt_identity()

    weeks = {
        "W1": 0,
        "W2": 0,
        "W3": 0,
        "W4": 0
    }

    transactions = Transaction.query.filter_by(
        user_id=user_id,
        type="debit"
    ).all()

    for transaction in transactions:

        day = transaction.date.day

        if day <= 7:
            weeks["W1"] += transaction.amount
        elif day <= 14:
            weeks["W2"] += transaction.amount
        elif day <= 21:
            weeks["W3"] += transaction.amount
        else:
            weeks["W4"] += transaction.amount

    return jsonify([
        {
            "week": week,
            "amount": amount
        }
        for week, amount in weeks.items()
    ])