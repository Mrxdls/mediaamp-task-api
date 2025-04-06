from flask import request, jsonify, Blueprint
from APP.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from datetime import timedelta
from APP import db
from werkzeug.security import generate_password_hash, check_password_hash
from APP.schemas import UserSchema, loginUserSchema
from APP.Services.rate_limiter import limiter

user_blueprint = Blueprint('users', __name__)
@user_blueprint.route('/register', methods=['POST'])
@jwt_required()
def register_user():
    current_user_identity = get_jwt_identity()
    Current_user = User.query.filter_by(id=current_user_identity['id']).first()
    if not Current_user or Current_user.role != 'admin':
        return jsonify({"error": "You are not authorized to register users."}), 403
    data = request.get_json()
    try:
        validate_data = UserSchema(**data)
    except Exception as e:
        print(f"Error while validating data: {e}")

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            "error": "Invalid input. Please provide a JSON object with 'username' and 'password'.",
            "example": {
                "username": "your_username",
                "password": "your_password",
                "role": "user/admin"
            }
        }), 400

    username = data.get('username')
    if User.query.filter_by(username= validate_data.username).first():
        return jsonify({"error": "Username already exists"}), 409

    # Convert password to hash
    hash_pass = generate_password_hash(validate_data.password)
    password = hash_pass
    role = data.get('role', 'user')

    # Insert new user into the database
    new_user = User(username=validate_data.username,
                    password=validate_data.password,
                    role=validate_data.role)
    db.session.add(new_user)
    try:
        db.session.commit()
    except Exception as e:
        print(f"Error while committing to the database: {e}")
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "username": username,
            "password": password,
            # in real application, do not return password
            # "password": hash_pass
            "role": role
        }
    }), 201


@user_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    try:
        validate_data = loginUserSchema(**data)
    except Exception as e:
        print(f"Error while validating data: {e}")
        return jsonify({"error": "Invalid input"}), 400
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            "error": "Invalid input. Please provide a JSON object with 'username' and 'password'.",
            "example": {
                "username": "your_username",
                "password": "your_password"
            }
        }), 400

    username = validate_data.username
    password = validate_data.password

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity={"id": user.id, "username": username}, expires_delta=timedelta(days=1))
        return jsonify({
            "message": "Login successful",
            "access_token": access_token
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    


@user_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_identity = get_jwt_identity()
    user = User.query.filter_by(id=current_user_identity['id']).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "username": user.username,
        "role": user.role
    }), 200

