#!/usr/bin/python3
""" Places views for RESTFul API actions """
from api.v1.views import app_views
from flask import make_response, jsonify, request, abort
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_citie_places(city_id):
    """ Get all places in city with city id """
    city = storage.get('City', city_id)
    if city:
        places_list = [place.to_dict() for place in city.places]
        return make_response(jsonify(places_list))
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ POST a new place to the database """
    city = storage.get('City', city_id)
    if city:
        from models.place import Place
        data = request.get_json()
        if not data:
            return abort(400, 'Not a JSON')
        elif 'user_id' not in data:
            return abort(400, 'Missing user_id')
        elif storage.get('User', data['user_id']) is None:
            return abort(404)
        elif 'name' not in data:
            return abort(400, 'Missing name')
        data.update({'city_id': city_id})
        place = Place(**data)
        place.save()
        return make_response(jsonify(place.to_dict()), 201)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ GET place based on its id """
    place = storage.get('Place', place_id)
    if place:
        return make_response(jsonify(place.to_dict()))
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ DELETE place based on its id """
    place = storage.get('Place', place_id)
    if place:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get('Place', place_id)
    if place:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        ignor_list = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, val in data.items():
            if key not in ignor_list:
                setattr(place, key, val)
        place.save()
        return make_response(jsonify(place.to_dict()), 200)
    else:
        abort(404)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def place_search():
    """function to search places based on the json in the request"""
    body = request.get_json()

    if body is None:
        abort(400, 'Not a JSON')

    states = body.get('states', [])
    cities = body.get('cities', [])
    amenities = body.get('amenities', [])

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        places_list = [place.to_dict() for place in places]
        return jsonify(places_list)

    unique_places = set()

    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                state_cities = state.cities
                for city in state_cities:
                    if city:
                        places = city.places
                        for place in places:
                            if place:
                                unique_places.add(place)

    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places = city.places
                for place in places:
                    if place:
                        unique_places.add(place)

    filtered_places = set(unique_places)

    if amenities:
        for amenity_id in amenities:
            for place in filtered_places.copy():
                place_amenities = place.amenities
                if not all(amenity.id == amenity_id
                           for amenity in place_amenities):
                    filtered_places.remove(place)

    found_places = [place.to_dict() for place in filtered_places]

    return jsonify(found_places)
