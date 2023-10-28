#!/usr/bin/python3
""" Flask web app api """
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found_error(exception):
    """ “404 page”, a “Not found” """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown_storage(exception):
    """ Closes the storage on teardown """
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', 5000)), threaded=True)
