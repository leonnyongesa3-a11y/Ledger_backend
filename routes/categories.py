from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.category import Category

categories_bp = Blueprint("categories", __name__)

@categories_bp.route("/", methods=["GET"])
@jwt_required()
def get_categories():

    user_id = get_jwt_identity()

    categories = Category.query.filter_by(
        user_id=user_id
    ).order_by(Category.name).all()

    return jsonify([
        category.to_dict()
        for category in categories
    ]), 200

@categories_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_category(id):

    user_id = get_jwt_identity()

    category = Category.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if not category:
        return jsonify({
            "error": "Category not found."
        }), 404

    return jsonify(category.to_dict()), 200

@categories_bp.route("/", methods=["POST"])
@jwt_required()
def create_category():

    user_id = get_jwt_identity()

    data = request.get_json()

    name = data.get("name")

    if not name:
        return jsonify({
            "error": "Category name is required."
        }), 400

    existing = Category.query.filter_by(
        name=name,
        user_id=user_id
    ).first()

    if existing:
        return jsonify({
            "error": "Category already exists."
        }), 409

    category = Category(
        name=name,
        user_id=user_id
    )

    db.session.add(category)
    db.session.commit()

    return jsonify(category.to_dict()), 201

@categories_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_category(id):

    user_id = get_jwt_identity()

    category = Category.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if not category:
        return jsonify({
            "error": "Category not found."
        }), 404

    data = request.get_json()

    if "name" in data:
        category.name = data["name"]

    db.session.commit()

    return jsonify(category.to_dict()), 200

@categories_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_category(id):

    user_id = get_jwt_identity()

    category = Category.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if not category:
        return jsonify({
            "error": "Category not found."
        }), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({
        "message": "Category deleted successfully."
    }), 200