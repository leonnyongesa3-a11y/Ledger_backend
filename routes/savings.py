from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from extensions import db
from models.savings_goal import SavingsGoal

savings_bp = Blueprint("savings", __name__)


# GET ALL SAVINGS GOALS
@savings_bp.route("/", methods=["GET"])
@jwt_required()
def get_savings_goals():

    user_id = get_jwt_identity()

    goals = SavingsGoal.query.filter_by(
        user_id=user_id
    ).all()

    return jsonify([
        goal.to_dict()
        for goal in goals
    ]), 200


# GET ONE SAVINGS GOAL
@savings_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_savings_goal(id):

    user_id = get_jwt_identity()

    goal = SavingsGoal.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if not goal:
        return jsonify({
            "error": "Savings goal not found."
        }), 404

    return jsonify(goal.to_dict()), 200


# CREATE SAVINGS GOAL
@savings_bp.route("/", methods=["POST"])
@jwt_required()
def create_goal():

    user_id = get_jwt_identity()
    data = request.get_json()

    if not data.get("name") or not data.get("target"):
        return jsonify({
            "error": "Goal name and target amount are required."
        }), 400

    goal = SavingsGoal(
        name=data["name"],
        target_amount=float(data["target"]),
        saved_amount=float(data.get("saved", 0)),
        color=data.get("color", "#10d876"),
        note=data.get("note"),
        deadline=(
            datetime.strptime(
                data["deadline"],
                "%Y-%m-%d"
            ).date()
            if data.get("deadline")
            else None
        ),
        user_id=user_id
    )

    db.session.add(goal)
    db.session.commit()

    return jsonify(goal.to_dict()), 201


# UPDATE SAVINGS GOAL
@savings_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_goal(id):

    user_id = get_jwt_identity()

    goal = SavingsGoal.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if not goal:
        return jsonify({
            "error": "Savings goal not found."
        }), 404

    data = request.get_json()

    if "name" in data:
        goal.name = data["name"]

    if "target" in data:
        goal.target_amount = float(data["target"])

    if "saved" in data:
        goal.saved_amount = float(data["saved"])

    if "color" in data:
        goal.color = data["color"]

    if "note" in data:
        goal.note = data["note"]

    if "deadline" in data:
        goal.deadline = (
            datetime.strptime(
                data["deadline"],
                "%Y-%m-%d"
            ).date()
            if data["deadline"]
            else None
        )

    db.session.commit()

    return jsonify(goal.to_dict()), 200


# DELETE SAVINGS GOAL
@savings_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_goal(id):

    user_id = get_jwt_identity()

    goal = SavingsGoal.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if not goal:
        return jsonify({
            "error": "Savings goal not found."
        }), 404

    db.session.delete(goal)
    db.session.commit()

    return jsonify({
        "message": "Savings goal deleted successfully."
    }), 200