from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.budget import Budget

budgets_bp = Blueprint("budgets", __name__)

@budgets_bp.route("/", methods=["GET"])
@jwt_required()
def get_budgets():

    user_id = get_jwt_identity()

    budgets = Budget.query.filter_by(
        user_id=user_id
    ).order_by(Budget.category).all()

    return jsonify([
        budget.to_dict()
        for budget in budgets
    ]), 200

@budgets_bp.route("/", methods=["POST"])
@jwt_required()
def create_budget():

    user_id = get_jwt_identity()

    data = request.get_json()

    budget = Budget(
        category=data["category"],
        spent=data.get("spent", 0),
        limit_amount=data.get("limit", 0),
        color=data["color"],
        user_id=user_id
    )

    db.session.add(budget)
    db.session.commit()

    return jsonify(budget.to_dict()), 201

@budgets_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_budget(id):

    user_id = get_jwt_identity()

    budget = Budget.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if not budget:
        return jsonify({
            "error": "Budget not found."
        }), 404

    data = request.get_json()

    if "category" in data:
        budget.category = data["category"]

    if "spent" in data:
        budget.spent = float(data["spent"])

    if "limit" in data:
        budget.limit_amount = float(data["limit"])

    if "color" in data:
        budget.color = data["color"]

    db.session.commit()

    return jsonify(budget.to_dict()), 200

@budgets_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_budget(id):

    user_id = get_jwt_identity()

    budget = Budget.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if not budget:
        return jsonify({
            "error": "Budget not found."
        }), 404

    db.session.delete(budget)
    db.session.commit()

    return jsonify({
        "message": "Budget deleted successfully."
    }), 200