# app/routes/auth.py
from flask import Blueprint, request, jsonify
from .. import db
from ..models import User
from ..services.auth_service import hash_password, check_password, generate_tokens, revoke_token
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"msg": "Email and password required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 409
    user = User(email=email, password_hash=hash_password(password))
    db.session.add(user)
    db.session.commit()
    return jsonify(generate_tokens(user.id)), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"msg": "Email and password required"}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not check_password(password, user.password_hash):
        return jsonify({"msg": "Invalid credentials"}), 401
    return jsonify(generate_tokens(user.id)), 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = generate_tokens(identity)["access_token"]
    return jsonify({"access_token": access_token}), 200

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    revoke_token(jti)
    return jsonify({"msg": "Logged out"}), 200
