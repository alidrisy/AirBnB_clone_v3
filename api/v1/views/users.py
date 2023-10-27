#!/usr/bin/python3
""" User model that handles all default RESTFul API actions """
from api.v1.views import app_views
from models import storage
from flask import jsonify, make_response, abort, request


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users(user_id=None):
    """ GET users or user by id """
    if user_id:
        user = storage.get('User', user_id)
        if user:
            return make_response(jsonify(user.to_dict()))
        else:
            abort(404)
    users = storage.all('User')
    data = [user.to_dict() for user in users.values()]
    return make_response(jsonify(data))


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get('User', user_id)
    if user:
        storage.delete(user)
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a User """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    elif 'email' not in data:
        abort(400, 'Missing email')
    elif 'password' not in data:
        abort(400, 'Missing password')
    from models.user import User
    user = User()
    [setattr(user, k, v) for k, v in data.items()]
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object """
    user = storage.get('User', user_id)
    if user:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for k, v in data.items():
            if k not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, k, v)
        user.save()
        return make_response(jsonify(user.to_dict()), 200)
    else:
        abort(404)
