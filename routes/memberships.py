from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mysql

memberships_bp = Blueprint('memberships', __name__)

@memberships_bp.route('/groups/<int:group_id>/join', methods=['POST'])
@jwt_required()
def join_group(group_id):
    user_id = get_jwt_identity()
    cur = mysql.connection.cursor()

    cur.execute("SELECT max_members FROM groups_table WHERE id = %s", (group_id,))
    group = cur.fetchone()
    cur.execute("SELECT COUNT(*) FROM memberships WHERE group_id = %s", (group_id,))
    count = cur.fetchone()[0]

    if count >= group[0]:
        return jsonify({"error": "Group is full"}), 400

    cur.execute("SELECT id FROM memberships WHERE user_id=%s AND group_id=%s", (user_id, group_id))
    if cur.fetchone():
        return jsonify({"error": "Already a member"}), 400

    cur.execute("INSERT INTO memberships (user_id, group_id) VALUES (%s,%s)", (user_id, group_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Joined successfully"}), 201

@memberships_bp.route('/groups/<int:group_id>/leave', methods=['DELETE'])
@jwt_required()
def leave_group(group_id):
    user_id = get_jwt_identity()
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM memberships WHERE user_id=%s AND group_id=%s", (user_id, group_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Left group"}), 200

@memberships_bp.route('/my-groups', methods=['GET'])
@jwt_required()
def my_groups():
    user_id = get_jwt_identity()
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT g.* FROM groups_table g
        JOIN memberships m ON g.id = m.group_id
        WHERE m.user_id = %s
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    columns = ['id','title','course','description','max_members','schedule','location','creator_id']
    return jsonify([dict(zip(columns, r)) for r in rows]), 200