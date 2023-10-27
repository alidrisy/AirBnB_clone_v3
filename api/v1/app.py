#!/usr/bin/python3
""" Flask web app """
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

if getenv('HBNB_API_HOST'):
    host = getenv('HBNB_API_HOST')
else:
    host = '0.0.0.0'
if getenv('HBNB_API_PORT'):
    port = getenv('HBNB_API_PORT')
else:
    port = 5000


@app.teardown_appcontext
def teardown(exception):
    """ Closes the storage on teardown """
    storage.close()


if __name__ == "__main__":
    app.run(host, port)
