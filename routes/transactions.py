from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.transaction import Transaction
from models.category import Category

transactions_bp = Blueprint("transactions", __name__)

@transactions_bp.route("/", methods=["GET"])
@jwt_required()
def get_transactions():

    user_id = get_jwt_identity()

    transactions = (
        Transaction.query
        .filter_by(user_id=user_id)
        .order_by(Transaction.date.desc())
        .all()
    )

    return jsonify([t.to_dict() for t in transactions]), 200

@transactions_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_transaction(id):

    user_id = get_jwt_identity()

    transaction = Transaction.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    return jsonify(transaction.to_dict()), 200

@transactions_bp.route("/", methods=["POST"])
@jwt_required()
def create_transaction():

    user_id = get_jwt_identity()

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
        user_id=user_id
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
        user_id=user_id,
        category_id=category.id
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify(transaction.to_dict()), 201

@transactions_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_transaction(id):

    user_id = get_jwt_identity()

    transaction = Transaction.query.filter_by(
        id=id,
        user_id=user_id
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
            user_id=user_id
        ).first()

        if not category:
            return jsonify({
                "error": "Category not found."
            }), 404

        transaction.category_id = "category.id"

    db.session.commit()

    return jsonify(transaction.to_dict()), 200

@transactions_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_transaction(id):

    user_id = get_jwt_identity()

    transaction = Transaction.query.filter_by(
        id=id,
        user_id=user_id
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