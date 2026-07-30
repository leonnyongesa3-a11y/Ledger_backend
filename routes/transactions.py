from datetime import datetime

from flask import Blueprint, jsonify, request

from extensions import db
from models.transaction import Transaction
from models.category import Category

transactions_bp = Blueprint("transactions", __name__)

@transactions_bp.route("", methods=["GET"])
def get_transactions():


    transactions = (
        Transaction.query.order_by(Transaction.date.desc())
        .all()
    )

    return jsonify([t.to_dict() for t in transactions]), 200

@transactions_bp.route("/<int:id>", methods=["GET"])
def get_transaction(id):

    transaction = Transaction.query.filter_by(
        id=id,
    ).first()

    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    return jsonify(transaction.to_dict()), 200

@transactions_bp.route("", methods=["POST"])
def create_transaction():


    data = request.get_json()

    merchant = data.get("merchant")
    amount = data.get("amount")
    tx_type = data.get("type")
    date = data.get("date")
    category_name = data.get("category")

    if not all([merchant, amount, tx_type, date, category_name]):
        return jsonify({
            "error": "All fields are required."
        }), 400

    category = Category.query.filter_by(
        id=category_name,
    ).first()

    if not category:
        return jsonify({
            "error": f"Category '{category_name}' not found."
        }), 404

    transaction = Transaction(
        merchant=merchant,
        amount=float(amount),
        type=tx_type,
        date=datetime.strptime(
            date,
            "%Y-%m-%d"
        ).date(),
        category_id=category.id
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify(transaction.to_dict()), 201

@transactions_bp.route("/<int:id>", methods=["PATCH"])
def update_transaction(id):


    transaction = Transaction.query.filter_by(
        id=id,
    ).first()

    if not transaction:
        return jsonify({
            "error": "Transaction not found."
        }), 404

    data = request.get_json()

    if "merchant" in data:
        transaction.merchant = data["merchant"]

    if "amount" in data:
        transaction.amount = float(data["amount"])

    if "type" in data:
        transaction.type = data["type"]

    if "date" in data:
        transaction.date = datetime.strptime(
            data["date"],
            "%Y-%m-%d"
        ).date()

    if "category" in data:

        category = Category.query.filter_by(
            id=data["category"],
        ).first()

        if not category:
            return jsonify({
                "error": "Category not found."
            }), 404

        transaction.category_id = category.id

    db.session.commit()

    return jsonify(transaction.to_dict()), 200

@transactions_bp.route("/<int:id>", methods=["DELETE"])

def delete_transaction(id):

    transaction = Transaction.query.filter_by(
        id=id,
    ).first()

    if not transaction:
        return jsonify({
            "error": "Transaction not found."
        }), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({
        "message": "Transaction deleted successfully."
    }), 200