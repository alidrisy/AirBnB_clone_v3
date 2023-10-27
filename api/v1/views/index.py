#!/usr/bin/python3
""" Flask web templet """
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Returns a JSON status """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def print_count():
    """Return the count of all classes in json format"""
    stats = {}

    class_names = {
            "states": "State",
            "cities": "City",
            "amenities": "Amenity",
            "places": "Place",
            "reviews": "Review",
            "users": "User"
            }

    for class_name in class_names:
        stats[class_name] = storage.count(class_names[class_name])

    return make_response(jsonify(stats))
