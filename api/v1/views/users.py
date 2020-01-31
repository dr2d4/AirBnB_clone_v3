#!/usr/bin/python3
""" Users Views """
from flask import jsonify, abort, request

from api.v1.views import app_views

from models.user import User

from models import storage


@app_views.route('/users', methods=['POST'])
def create_user():
    """
        Create new User
    """
    r_json = request.get_json()

    if not r_json:
        abort(400, "Not a JSON")
    elif not r_json.get('email'):
        abort(400, 'Missing email')
    elif not r_json.get('password'):
        abort(400, 'Missing password')

    nobj = User(**r_json)
    nobj.save()

    nobj = nobj.to_dict()
    return jsonify(nobj), 201


app_views.route('/users', methods=['GET'])
def all_users():
    """
        Get all Users
    """
    users = storage.all('User')
    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
        Get User by Id
    """
    user = storage.get('User', user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def del_user(user_id):
    """
        Delete User by Id
    """
    user = storage.get('User', user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    """
        Update User by Id
    """
    r_json = request.get_json()
    if not r_json:
        abort(400, "Not a JSON")
    objs = storage.all('User')
    for user in objs.values():
        if user.id == user_id:
            r_json.pop('created_at', 0)
            r_json.pop('updated_at', 0)
            r_json.pop('id', 0)
            r_json.pop('email', 0)
            for attr in r_json:
                if hasattr(user, attr):
                    user.__setattr__(attr, r_json[attr])
            user.save()
            return jsonify(user.to_dict())
    abort(404)
