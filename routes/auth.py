from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from extensions import mysql, bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    department = data.get('department', '')
    level = data.get('level', '')

    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "INSERT INTO users (name, email, password, department, level) VALUES (%s,%s,%s,%s,%s)",
            (name, email, password, department, level)
        )
        mysql.connection.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, password FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.check_password_hash(user[1], data['password']):
        token = create_access_token(identity=str(user[0]))
        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid credentials"}), 401