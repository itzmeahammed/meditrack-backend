import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from models import mongo, bcrypt
from flask import current_app

# Set up a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# Secret key for encoding JWT tokens
SECRET_KEY = "your-secret-key"  # Replace with your actual secret key

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    # Find the user from the database by email
    user = mongo.db.users.find_one({"email": email})
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Generate JWT token with role included in the claims
    payload = {
        "sub": email,  # subject of the token (email)
        "role": user['role'],  # Add role to the claims
        "iat": datetime.utcnow(),  # issued at time
        "exp": datetime.utcnow() + timedelta(days=1)  # expiration time (1 day)
    }

    # Encode the JWT token using PyJWT
    access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify(
        access_token=access_token,
        role=user['role']  # Return the role explicitly as well
    ), 200


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Extract data from the request
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    mobile = data.get('mobile')
    role = data.get('role')
    secret_code = data.get('secretCode')

    # Admin Secret Code Validation (for admin role only)
    if role == 'admin' and secret_code != "1234":
        return jsonify({"message": "Invalid admin secret code."}), 400

    if mongo.db.users.find_one({"email": email}):
        return jsonify({"message": "User already exists."}), 400
    
    # Hash password before storing
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = {
        "email": email,
        "password": hashed_password,
        "username": username,
        "role": role,
        "mobile": mobile
    }

    # Insert user into MongoDB
    mongo.db.users.insert_one(user)
    
    return jsonify({"message": "User created successfully."}), 201
