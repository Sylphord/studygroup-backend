from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mysql

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/groups', methods=['POST'])
@jwt_required()
def create_group():
    user_id = get_jwt_identity()
    data = request.get_json()

    cur = mysql.connection.cursor()
    cur.execute(
        """INSERT INTO groups_table (title, course, description, max_members, schedule, location, creator_id)
           VALUES (%s,%s,%s,%s,%s,%s,%s)""",
        (data['title'], data['course'], data['description'],
         data['max_members'], data['schedule'], data['location'], user_id)
    )
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Group created"}), 201

@groups_bp.route('/groups', methods=['GET'])
def get_groups():
    course = request.args.get('course')
    cur = mysql.connection.cursor()

    if course:
        cur.execute("SELECT * FROM groups_table WHERE course = %s", (course,))
    else:
        cur.execute("SELECT * FROM groups_table")

    rows = cur.fetchall()
    cur.close()

    columns = ['id','title','course','description','max_members','schedule','location','creator_id']
    groups = [dict(zip(columns, row)) for row in rows]
    return jsonify(groups), 200

@groups_bp.route('/groups/<int:group_id>', methods=['DELETE'])
@jwt_required()
def delete_group(group_id):
    user_id = get_jwt_identity()
    cur = mysql.connection.cursor()
    cur.execute("SELECT creator_id FROM groups_table WHERE id = %s", (group_id,))
    group = cur.fetchone()

    if not group:
        return jsonify({"error": "Group not found"}), 404
    if str(group[0]) != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    cur.execute("DELETE FROM groups_table WHERE id = %s", (group_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Group deleted"}), 200