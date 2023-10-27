#!/usr/bin/python3
""" Flask web templet """
from api.v1.views import app_views
from flask import jsonify, make_response


@app_views.route('/status', strict_slashes=False)
def states():
    """ Returns a JSON status """
    return make_response(jsonify({"status": "OK"}))
