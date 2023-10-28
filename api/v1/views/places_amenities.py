#!/usr/bin/python3
""" API views for Place - Amenity objects relationship """
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from models import storage
from os import getenv

type_storage = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """ GET amenities based on place id """
    place = storage.get('Place', place_id)
    if place:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            amenities = place.amenities
        else:
            ids = place.amenity_ids
            amenities = [storage.get('Place', id1) for id1 in ids]
        list_amenities = [amenity.to_dict() for amenity in amenities]
        return make_response(jsonify(list_amenities))
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place_amenity(place_id, amenity_id):
    """ DELETE amenity from place based on place and amenity ids """
    place = storage.get('Place', place_id)
    if place:
        amenity = storage.get('Amenity', amenity_id)
        if amenity and amenity in place.amenities:
            if type_storage == 'db':
                place.amenities.remove(amenity)
            else:
                place.amenity_ids.remove(amenity.id)
            place.save()
            return make_response(jsonify({}), 200)
        else:
            abort(404)
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def like_amenity_place(place_id, amenity_id):
    """ Link a Amenity object to a Place """
    place = storage.get('Place', place_id)
    if place:
        amenity = storage.get('Amenity', amenity_id)
        if amenity:
            if amenity in place.amenities:
                return make_response(jsonify(amenity.to_dict()), 200)
            else:
                if type_storage == 'db':
                    place.amenities.append(amenity)
                else:
                    place.amenity_ids.append(amenity.id)
                place.save()
                return make_response(jsonify(amenity.to_dict()), 201)
        else:
            abort(404)
    else:
        abort(404)
