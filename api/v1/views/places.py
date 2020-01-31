#!/usr/bin/python3
""" Places Views """
from flask import jsonify, abort, request

from api.v1.views import app_views

from models.place import Place

from models import storage


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """
        Create new Place
    """
    if not storage.get('City', city_id):
        abort(404)
    if not storage.get('User', user_id):
        abort(404)
    r_json = request.get_json()

    if not r_json:
        abort(400, "Not a JSON")
    elif not r_json.get('user_id'):
        abort(400, 'Missing user_id')
    elif not r_json.get('name'):
        abort(400, 'Missing name')

    nobj = Place(city_id=city_id, **r_json)
    resp = nobj.to_dict()
    nobj.save()

    return jsonify(resp), 201


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def all_places(city_id):
    """
        Get all Places
    """
    city = storage.get('City', city_id)
    places_list = []
    if not city:
        abort(404)
    places = city.places
    for place in places:
        places_list.append(place.to_dict())

        return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """
        Get Place by Id
    """
    place = storage.get('Place', place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


app_views.route('/places/<place_id>', methods=['DELETE'])
def del_place(place_id):
    """
        Delete Place by Id
    """
    place = storage.get('Place', place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """
        Update Place by Id
    """
    r_json = request.get_json()
    if not r_json:
        abort(400, "Not a JSON")
    place = storage.get('Place', place_id)
    if place:
        r_json.pop('created_at', 0)
        r_json.pop('updated_at', 0)
        r_json.pop('id', 0)
        r_json.pop('user_id', 0)
        for attr in r_json:
            if hasattr(place, attr):
                place.__setattr__(attr, r_json[attr])
        place.save()
        return jsonify(place.to_dict())
    abort(404)
