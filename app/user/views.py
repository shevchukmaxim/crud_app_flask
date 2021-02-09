from flask import Blueprint, jsonify, request, make_response
from ..models import User
from .. import db
from flask_expects_json import expects_json

user = Blueprint('user', __name__)

user_validation_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'surname': {'type': 'string'}
    },
    'required': ['name', 'surname']
}


@user.route('/users', methods=['GET'])
def list_users():
    """
    List all users
    """
    users = [User.json(user) for user in User.query.all()]
    return make_response(jsonify(users))


@user.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """
    Get one user
    """
    user = User.query.get_or_404(id)
    return make_response(jsonify(user.json()))


@user.route('/users', methods=['POST'])
@expects_json(user_validation_schema)
def add_user():
    """
    Add user to the database
    """
    request_data = request.get_json()

    user = User(name=request_data['name'], surname=request_data['surname'])
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify(user.json()))


@user.route('/users/<int:id>', methods=['PUT'])
@expects_json(user_validation_schema)
def edit_user(id):
    """
    Edit user
    """
    request_data = request.get_json()
    user_to_update = User.query.get_or_404(id)
    user_to_update.name = request_data['name']
    user_to_update.surname = request_data['surname']
    db.session.commit()

    return make_response(jsonify(user_to_update.json()))


@user.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """
    Delete user from the database
    """

    User.query.filter_by(id=id).delete()

    db.session.commit()

    return make_response(jsonify({'status': 'success'}))
