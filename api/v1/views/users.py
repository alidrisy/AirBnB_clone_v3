#!/usr/bin/python3
""" User view for RESTFul API"""
from models import storage
from flask import request, jsonify, abort, make_response
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_users(user_id=None):
    """ Endpoint to get all users """
    if user_id is None:
        users = storage.all(User).values()
        users_list = [user.to_dict() for user in users]
        return jsonify(users_list)
    else:
        user = storage.get(User, user_id)
        if user:
            return jsonify(user.to_dict())
        else:
            abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user based on its ID"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Posts a new User to the database"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    elif "email" not in data:
        abort(400, "Missing email")
    elif "password" not in data:
        abort(400, "Missing password")
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a user using a PUT request"""
    user = storage.get(User, user_id)
    if user:
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")

        for key, value in data.items():
            if key not in ["email", "id", "created_at", "updated_at"]:
                setattr(user, key, value)
        user.save()
        return make_response(jsonify(user.to_dict()), 200)
    else:
        abort(404)
