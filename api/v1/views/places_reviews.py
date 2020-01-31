#!/usr/bin/python3
""" Reviews Views """
from flask import jsonify, abort, request

from api.v1.views import app_views

from models.review import Review

from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """
        Create new Review
    """
    if not storage.get('Place', place_id):
        abort(404)

    r_json = request.get_json()

    if not r_json:
        abort(400, "Not a JSON")
    elif not r_json.get('user_id'):
        abort(400, 'Missing user_id')
    elif not r_json.get('text'):
        abort(400, 'Missing text')

    if not storage.get('User', r_json.get('user_id')):
        abort(404)

    nobj = Review(**r_json)
    nobj.save()

    nobj = nobj.to_dict()
    return jsonify(nobj), 201


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def all_reviews(place_id):
    """
        Get all Reviews
    """
    place = storage.get('Place', place_id)
    reviews_list = []

    if not place:
        abort(404)

    reviews = place.reviews

    for review in reviews:
        reviews_list.append(review.to_dict())

    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """
        Get Reviews by Id
    """
    review = storage.get('Review', review_id)

    if review:
        return jsonify(review.to_dict())

    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def del_review(review_id):
    """
        Delete Review by Id
    """
    review = storage.get('Review', review_id)

    if review:
        storage.delete(review)
        storage.save()

        return jsonify({})

    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """
        Update Review by Id
    """
    r_json = request.get_json()

    if not r_json:
        abort(400, "Not a JSON")

    review = storage.get('Review', review_id)

    if review:
        r_json.pop('created_at', 0)
        r_json.pop('updated_at', 0)
        r_json.pop('place_id', 0)
        r_json.pop('user_id', 0)
        r_json.pop('id', 0)

        for attr in r_json:
            if hasattr(review, attr):
                review.__setattr__(attr, r_json[attr])

        review.save()

        return jsonify(review.to_dict())

    abort(404)
