from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/groups', methods=['POST'])
@jwt_required()
def create_group():
    user_id = get_jwt_identity()
    data = request.get_json()
    db.engine.execute(
        "INSERT INTO groups_table (title, course, description, max_members, schedule, location, creator_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (data['title'], data['course'], data['description'], data['max_members'], data['schedule'], data['location'], user_id)
    )
    return jsonify({"message": "Group created"}), 201

@groups_bp.route('/groups', methods=['GET'])
def get_groups():
    course = request.args.get('course')
    if course:
        result = db.engine.execute("SELECT * FROM groups_table WHERE course = %s", (course,))
    else:
        result = db.engine.execute("SELECT * FROM groups_table")
    columns = ['id','title','course','description','max_members','schedule','location','creator_id']
    groups = [dict(zip(columns, row)) for row in result]
    return jsonify(groups), 200

@groups_bp.route('/groups/<int:group_id>', methods=['DELETE'])
@jwt_required()
def delete_group(group_id):
    user_id = get_jwt_identity()
    result = db.engine.execute("SELECT creator_id FROM groups_table WHERE id = %s", (group_id,))
    group = result.fetchone()
    if not group:
        return jsonify({"error": "Group not found"}), 404
    if str(group[0]) != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    db.engine.execute("DELETE FROM groups_table WHERE id = %s", (group_id,))
    return jsonify({"message": "Group deleted"}), 200