from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db

memberships_bp = Blueprint('memberships', __name__)

@memberships_bp.route('/groups/<int:group_id>/join', methods=['POST'])
@jwt_required()
def join_group(group_id):
    user_id = get_jwt_identity()
    group = db.session.execute(db.text("SELECT max_members FROM groups_table WHERE id = :id"), {"id": group_id}).fetchone()
    count = db.session.execute(db.text("SELECT COUNT(*) FROM memberships WHERE group_id = :id"), {"id": group_id}).fetchone()[0]
    if count >= group[0]:
        return jsonify({"error": "Group is full"}), 400
    existing = db.session.execute(db.text("SELECT id FROM memberships WHERE user_id = :uid AND group_id = :gid"), {"uid": user_id, "gid": group_id}).fetchone()
    if existing:
        return jsonify({"error": "Already a member"}), 400
    db.session.execute(db.text("INSERT INTO memberships (user_id, group_id) VALUES (:uid, :gid)"), {"uid": user_id, "gid": group_id})
    db.session.commit()
    return jsonify({"message": "Joined successfully"}), 201

@memberships_bp.route('/groups/<int:group_id>/leave', methods=['DELETE'])
@jwt_required()
def leave_group(group_id):
    user_id = get_jwt_identity()
    db.session.execute(db.text("DELETE FROM memberships WHERE user_id = :uid AND group_id = :gid"), {"uid": user_id, "gid": group_id})
    db.session.commit()
    return jsonify({"message": "Left group"}), 200

@memberships_bp.route('/my-groups', methods=['GET'])
@jwt_required()
def my_groups():
    user_id = get_jwt_identity()
    result = db.session.execute(db.text("""
        SELECT g.* FROM groups_table g
        JOIN memberships m ON g.id = m.group_id
        WHERE m.user_id = :uid
    """), {"uid": user_id})
    columns = ['id','title','course','description','max_members','schedule','location','creator_id']
    return jsonify([dict(zip(columns, r)) for r in result]), 200