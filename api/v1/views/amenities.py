#!/usr/bin/python3
""" Amenitys Views """
from flask import jsonify, abort, request

from api.v1.views import app_views

from models.amenity import Amenity

from models import storage


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """
        Create new Amenity
    """
    r_json = request.get_json()

    if not r_json:
        abort(400, "Not a JSON")
    elif not r_json.get('name'):
        abort(400, 'Missing name')

    nobj = Amenity(**r_json)
    nobj.save()

    nobj = nobj.to_dict()
    return jsonify(nobj), 201


@app_views.route('/amenities', methods=['GET'])
def all_amenities():
    """
        Get all Amenitys
    """
    amenities = storage.all('Amenity')
    amenities_list = []

    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list)


@app_views.route('/amenites/<amenity_id>', methods=['GET'])
def get_state(state_id):
    """
        Get State by Id
    """
    amenity = storage.get('Amenity', amenity_id)

    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_amenity(amenity_id):
    """
        Delete Amenity by Id
    """
    amenity = storage.get('Amenity', amenity_id)

    if amenity:
        storage.delete(amenity)
        storage.save()

        return jsonify({})
    else:
        abort(404)
