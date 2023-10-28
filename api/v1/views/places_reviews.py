#!/usr/bin/python3
""" Reviews view for RESTFul API"""
from api.v1.views import app_views
from models import storage
from flask import Flask, request, jsonify, abort, make_response
from models.review import Review
from models.place import Place


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'])
def get_reviews_for_place(place_id):
    """function to get reviews for a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        places_reviews = storage.all(Review).values()
        reviews = [review.to_dict() for review in places_reviews
                   if review.place_id == place_id]
        return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review_by_id(review_id):
    """gets review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'])
def delete_review_by_id(review_id):
    """deletes review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_a_review(place_id):
    """creates a new review for a place"""
    body = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if body is None:
        abort(400, "Not a JSON")
    if "user_id" not in body:
        abort(400, "Missing user_id")

    user_id = body.get('user_id')

    if user_id is None:
        abort(404)

    if "text" not in body:
        abort(400, "Missing text")

    review = Review(**body)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_a_review(review_id):
    """updates a review by its id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    body = request.get_json()

    if body is None:
        abort(400, "Not a JSON")

    for key, value in body.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    return jsonify(review), 200
