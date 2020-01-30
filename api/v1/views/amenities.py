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

