from flask import Blueprint, jsonify, request
from models import db, Author, Book, Publisher

routes = Blueprint('routes', __name__)

@routes.route('/authors', methods=['POST'])
def create_author():
    data = request.json
    author = Author(name=data['name'])
    db.session.add(author)
    db.session.commit()
    return jsonify({"id": author.id, "name": author.name}), 201

@routes.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    author = Author.query.get_or_404(author_id)
    return jsonify({"id": author.id, "name": author.name})

@routes.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    return jsonify([{"id": a.id, "name": a.name} for a in authors])

@routes.route('/authors/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    data = request.json
    author = Author.query.get_or_404(author_id)
    author.name = data['name']
    db.session.commit()
    return jsonify({"id": author.id, "name": author.name})

@routes.route('/authors/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    return '', 204
