from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Bookmark

bookmarks_bp = Blueprint('bookmarks', __name__)

@bookmarks_bp.route('/', methods=['GET'])
@jwt_required()
def get_bookmarks():
    user_id = get_jwt_identity()
    bookmarks = Bookmark.query.filter_by(user_id=user_id).all()
    
    result = []
    for b in bookmarks:
        result.append({
            "id": b.id,
            "title": b.title,
            "url": b.url,
            "category": b.category,
            "description": b.description
        })
    return jsonify(result), 200

@bookmarks_bp.route('/', methods=['POST'])
@jwt_required()
def add_bookmark():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('url'):
        return jsonify({"msg": "Title and URL are required"}), 400
        
    new_bookmark = Bookmark(
        title=data.get('title'),
        url=data.get('url'),
        category=data.get('category'),
        description=data.get('description'),
        user_id=user_id
    )
    db.session.add(new_bookmark)
    db.session.commit()
    
    return jsonify({"msg": "Bookmark created successfully", "id": new_bookmark.id}), 201

@bookmarks_bp.route('/<int:bookmark_id>', methods=['GET'])
@jwt_required()
def get_bookmark(bookmark_id):
    user_id = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(id=bookmark_id, user_id=user_id).first()
    
    if not bookmark:
        return jsonify({"msg": "Bookmark not found"}), 404
        
    return jsonify({
        "id": bookmark.id,
        "title": bookmark.title,
        "url": bookmark.url,
        "category": bookmark.category,
        "description": bookmark.description
    }), 200

@bookmarks_bp.route('/<int:bookmark_id>', methods=['PUT'])
@jwt_required()
def update_bookmark(bookmark_id):
    user_id = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(id=bookmark_id, user_id=user_id).first()
    
    if not bookmark:
        return jsonify({"msg": "Bookmark not found"}), 404
        
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400
        
    if 'title' in data:
        bookmark.title = data['title']
    if 'url' in data:
        bookmark.url = data['url']
    if 'category' in data:
        bookmark.category = data['category']
    if 'description' in data:
        bookmark.description = data['description']
        
    db.session.commit()
    return jsonify({"msg": "Bookmark updated successfully"}), 200

@bookmarks_bp.route('/<int:bookmark_id>', methods=['DELETE'])
@jwt_required()
def delete_bookmark(bookmark_id):
    user_id = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(id=bookmark_id, user_id=user_id).first()
    
    if not bookmark:
        return jsonify({"msg": "Bookmark not found"}), 404
        
    db.session.delete(bookmark)
    db.session.commit()
    return jsonify({"msg": "Bookmark deleted successfully"}), 200
