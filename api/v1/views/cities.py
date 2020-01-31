#!/usr/bin/python3
""" Citys Views """
from flask import jsonify, abort, request

from api.v1.views import app_views

from models.city import City

from models import storage


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """
        Create new City
    """
    if not storage.get('State', state_id):
        abort(404)

    r_json = request.get_json()

    if not r_json:
        abort(400, "Not a JSON")
    elif not r_json.get('name'):
        abort(400, 'Missing name')

    nobj = City(state_id=state_id, **r_json)
    resp = nobj.to_dict()
    nobj.save()

    return jsonify(resp), 201


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def all_citys(state_id):
    """
        Get all Citys
    """
    state = storage.get('State', state_id)
    citys_list = []

    if not state:
        abort(404)

    citys = state.cities

    for city in citys:
        citys_list.append(city.to_dict())

    return jsonify(citys_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """
        Get City by Id
    """
    city = storage.get('City', city_id)

    if city:
        return jsonify(city.to_dict())

    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_city(city_id):
    """
        Delete City by Id
    """
    city = storage.get('City', city_id)

    if city:
        storage.delete(city)
        storage.save()

        return jsonify({})

    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city(city_id):
    """
        Update City by Id
    """
    r_json = request.get_json()

    if not r_json:
        abort(400, "Not a JSON")

    city = storage.get('City', city_id)

    if city:
        r_json.pop('created_at', 0)
        r_json.pop('updated_at', 0)
        r_json.pop('id', 0)

        for attr in r_json:
            if hasattr(city, attr):
                city.__setattr__(attr, r_json[attr])

        city.save()

        return jsonify(city.to_dict())

    abort(404)
