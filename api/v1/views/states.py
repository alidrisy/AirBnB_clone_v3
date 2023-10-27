#!/usr/bin/python3
""" States view for RESTFul API"""
from models.state import State
from models import storage
from flask import Flask, request, jsonify, abort, make_response
from api.v1.views import app_views


@app_views.route('/states/', strict_slashes=False, methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def show_states(state_id=None):
    """endpoint to get all states"""
    states = storage.all(State).values()
    if state_id is None:
        states_list = [state.to_dict() for state in states]
        return jsonify(states_list)
    else:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        else:
            return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Deletes a state based on its ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Posts a new state to the database"""
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    elif "name" not in body:
        abort(400, "Missing name")
    else:
        state = State(**body)
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """Updates a state using a PUT request"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        body = request.get_json()
        if body is None:
            abort(400, "Not a JSON")

        for key, value in body.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
