from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from extensions import db, bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    try:
        db.engine.execute(
            "INSERT INTO users (name, email, password, department, level) VALUES (%s,%s,%s,%s,%s)",
            (data['name'], data['email'], hashed, data.get('department',''), data.get('level',''))
        )
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    result = db.engine.execute("SELECT id, password FROM users WHERE email = %s", (data['email'],))
    user = result.fetchone()
    if user and bcrypt.check_password_hash(user[1], data['password']):
        token = create_access_token(identity=str(user[0]))
        return jsonify({"token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401