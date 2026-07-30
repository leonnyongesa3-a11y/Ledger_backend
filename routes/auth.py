from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "error": "All fields are required."
        }), 400

    existing = User.query.filter_by(email=email).first()

    if existing:
        return jsonify({
            "error": "Email already exists."
        }), 409

    user = User(
        name=name,
        email=email
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Account created successfully.",
        "user": user.to_dict()
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "error": "Invalid email or password."
        }), 401

    if not user.check_password(password):
        return jsonify({
            "error": "Invalid email or password."
        }), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful.",
        "token": token,
        "user": user.to_dict()
    }), 200

from flask_jwt_extended import jwt_required, get_jwt_identity


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    return jsonify(user.to_dict())

@auth_bp.route("/profile", methods=["PATCH"])
@jwt_required()
def update_profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    data = request.get_json()

    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    user.phone = data.get("phone", user.phone)
    user.country = data.get("country", user.country)
    user.currency = data.get("currency", user.currency)

    db.session.commit()

    return jsonify({
        "message": "Profile updated.",
        "user": user.to_dict()
    })