#!/usr/bin/env python3

import logging
import json

import connexion
from connexion import NoContent
from photo import Photo
from mongoengine import *
from bson.objectid import ObjectId
from bson import json_util
from bson.errors import InvalidId
import pymongo
from flask import jsonify
import json
import flask
import pprint
import base64
from io import BytesIO
from PIL import Image
import requests

from photo_mongo_wrapper import *

# See:
# https://devops.com/pymongo-pointers-make-robust-highly-available-mongo-queries
# for Robust Mongo Queries

def post_photo(display_name, image):
    try:
        # r = requests.get("http://127.0.0.1:8090" + "/photographer/" + display_name)
        r = requests.get('http://photographer-service:8090/photographer/' + display_name)
        if r.status_code != 200:
            return 'Photographer not found', 404

        ph = mongo_add(display_name, photo=image)
        # ph = mongo_add(display_name, photo=body)
        return 'Created', 201, {'location': '/photo/' + str(display_name) + '/' + str(ph.id)}
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.NetworkTimeout) as e:
        return 'Mongo unavailable', 503

def get_photos(display_name, offset, limit):
    try:
        # r = requests.get("http://127.0.0.1:8090" + "/photographer/" + display_name)
        r = requests.get('http://photographer-service:8090/photographer/' + display_name)
        if r.status_code != 200:
            return 'Photographer not found', 404

        json_array = []
        (has_more, list_of_photos) = mongo_get_photos(display_name, offset, limit)
        for ph in list_of_photos:
            json_data = {}
            json_data['link'] = flask.request.url_root + 'photo/' + str(display_name) + '/' + str(ph.id)
            json_array.append(json_data)
        # return json_array, 200, {'Content-Type': 'application/json'}
    except:
        return 'Not Found', 404
    return {'items': json_array, 'has_more': has_more}

def get_photo_by_id(display_name, photo_id):
    try:
        # r = requests.get("http://127.0.0.1:8090" + "/photographer/" + display_name)
        r = requests.get('http://photographer-service:8090/photographer/' + display_name)
        if r.status_code != 200:
            return 'Photographer not found', 404

        ph = mongo_get_photo_by_id(display_name, photo_id)
        photo = ph.photo.read()
        return photo, 200, {'Content-Type': 'image/jpeg'}
    except:
        return 'Not Found', 404

def delete_photo_by_id(display_name, photo_id):
    try:
        # r = requests.get("http://127.0.0.1:8090" + "/photographer/" + display_name)
        r = requests.get('http://photographer-service:8090/photographer/' + display_name)
        if r.status_code != 200:
            return 'Photographer not found', 404

        r_photo = requests.get(flask.request.url_root + 'photo/' + display_name + '/' + photo_id)
        if r_photo.status_code != 200:
            return 'Photo not found', 404

        ph = mongo_delete_photo_by_id(display_name, photo_id)
        if ph:
            return 'NoContent', 204
        else:
            return 'Not Found', 404
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.NetworkTimeout) as e:
        return 'Mongo unavailable', 503

def get_attributes_by_id(display_name, photo_id):
    try:
        # r = requests.get("http://127.0.0.1:8090" + "/photographer/" + display_name)
        r = requests.get('http://photographer-service:8090/photographer/' + display_name)
        if r.status_code != 200:
            return 'Photographer not found', 404

        att = mongo_get_attributes_by_id(display_name, photo_id)
        return att, 200, {'Content-Type': 'application/json'}
    except:
        return 'Not Found', 404

def set_attributes_by_id(display_name, photo_id, body):
    att = body
    try:
        # r = requests.get("http://127.0.0.1:8090" + "/photographer/" + display_name)
        r = requests.get('http://photographer-service:8090/photographer/' + display_name)
        if r.status_code != 200:
            return 'Photographer not found', 404

        photo = mongo_set_attributes_by_id(display_name, photo_id, att)
        return att, 201, {'Content-Type': 'application/json'}
    except:
        return 'Not Found', 404



