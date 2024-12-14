from flask import Blueprint, jsonify, request
from models import db, Author, User  # Make sure User model exists
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

# Define the blueprint
routes = Blueprint('routes', __name__)

# Route for user login
@routes.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if user exists and password matches
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        # Create JWT token
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid credentials"}), 401

# Route for user logout (JWT tokens are stateless, so it's just a placeholder)
@routes.route('/logout', methods=['POST'])
@jwt_required()  # Protect this route with JWT
def logout():
    return jsonify({"msg": "Successfully logged out"}), 200

# Protect existing routes with JWT authentication

@routes.route('/authors', methods=['POST'])
@jwt_required()
def create_author():
    data = request.json
    author = Author(name=data['name'])
    db.session.add(author)
    db.session.commit()
    return jsonify({"id": author.id, "name": author.name}), 201

@routes.route('/authors/<int:author_id>', methods=['GET'])
@jwt_required()
def get_author(author_id):
    author = Author.query.get_or_404(author_id)
    return jsonify({"id": author.id, "name": author.name})

@routes.route('/authors', methods=['GET'])
@jwt_required()
def get_authors():
    authors = Author.query.all()
    return jsonify([{"id": a.id, "name": a.name} for a in authors])

@routes.route('/authors/<int:author_id>', methods=['PUT'])
@jwt_required()
def update_author(author_id):
    data = request.json
    author = Author.query.get_or_404(author_id)
    author.name = data['name']
    db.session.commit()
    return jsonify({"id": author.id, "name": author.name})

@routes.route('/authors/<int:author_id>', methods=['DELETE'])
@jwt_required()
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    return '', 204
