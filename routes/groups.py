from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/groups', methods=['POST'])
@jwt_required()
def create_group():
    user_id = get_jwt_identity()
    data = request.get_json()
    db.session.execute(db.text(
        "INSERT INTO groups_table (title, course, description, max_members, schedule, location, creator_id) VALUES (:title, :course, :description, :max_members, :schedule, :location, :creator_id)"
    ), {**data, "creator_id": user_id})
    db.session.commit()
    return jsonify({"message": "Group created"}), 201

@groups_bp.route('/groups', methods=['GET'])
def get_groups():
    course = request.args.get('course')
    if course:
        result = db.session.execute(db.text("SELECT * FROM groups_table WHERE course = :course"), {"course": course})
    else:
        result = db.session.execute(db.text("SELECT * FROM groups_table"))
    columns = ['id','title','course','description','max_members','schedule','location','creator_id']
    groups = [dict(zip(columns, row)) for row in result]
    return jsonify(groups), 200

@groups_bp.route('/groups/<int:group_id>', methods=['DELETE'])
@jwt_required()
def delete_group(group_id):
    user_id = get_jwt_identity()
    result = db.session.execute(db.text("SELECT creator_id FROM groups_table WHERE id = :id"), {"id": group_id})
    group = result.fetchone()
    if not group:
        return jsonify({"error": "Group not found"}), 404
    if str(group[0]) != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    db.session.execute(db.text("DELETE FROM groups_table WHERE id = :id"), {"id": group_id})
    db.session.commit()
    return jsonify({"message": "Group deleted"}), 200