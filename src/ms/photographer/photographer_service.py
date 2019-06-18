#!/usr/bin/env python3

import logging
import json

import connexion
from connexion import NoContent
from photographer import Photographer
from mongoengine import *
from bson.objectid import ObjectId
from bson import json_util
from bson.errors import InvalidId
import pymongo
from flask import jsonify
import json
import flask
import pprint

from photographer_mongo_wrapper import *

# See:
# https://devops.com/pymongo-pointers-make-robust-highly-available-mongo-queries
# for Robust Mongo Queries

def get_photographers(offset, limit):
    list_of_photographers = list()
    try:
        (has_more, photographers) = mongo_get_photographers(offset, limit)
        for ph in photographers:
            ph._data.pop('id')
            ph._data.pop('first_name')
            ph._data.pop('last_name')
            ph._data.pop('interests')
            ph._data['link'] = flask.request.url_root + "photographer/" + str(ph.display_name)
            list_of_photographers.append(ph._data)
    except pymongo.errors.ServerSelectionTimeoutError as sste:
        return 503
    return {'items': list_of_photographers, 'has_more': has_more}

def get_photographer(display_name):
    logging.debug('Getting photographer with name: ' + display_name)
    try:
        ph = mongo_get_photographer_by_name(display_name)
        ph._data.pop('id') # This is not very clean ...
    except (Photographer.DoesNotExist, InvalidId) as e:
        return 'Not Found', 404
    except pymongo.errors.ServerSelectionTimeoutError as sste:
        return 'Mongo unavailable', 503
    return json.loads(json.dumps(ph._data, indent=4, default=json_util.default))

def post_photographers(body):
    photographer = body
    try:                                                                        
        if mongo_check(photographer['display_name']) > 0:                       
            return 'Conflict', 409                                              
        else:                                                                   
            ph = mongo_add (photographer['display_name'],                       
                            photographer['first_name'],                         
                            photographer['last_name'],                          
                            photographer['interests'])                          
            return 'Created', 201, {'location': '/photographer/' + str(ph.display_name)} 
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.NetworkTimeout) as e:
        return 'Mongo unavailable', 503                                                 

def delete_photographer(display_name):
    try:
        ph = mongo_delete_photographer_by_name(display_name)
        if ph:
            return 'NoContent', 204
        else:
            return 'Not Found', 404
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.NetworkTimeout) as e:
        return 'Mongo unavailable', 503                                                 

def put_photographer(display_name, body):
    logging.debug('Getting photographer with name: ' + display_name)
    photographer = body
    try:
        if mongo_check(display_name) == 0:
            return 'Not Found', 404
        else:
            ph = mongo_update_photographers_by_name(photographer['display_name'],
                                                    photographer['first_name'],
                                                    photographer['last_name'],
                                                    photographer['interests'])
            return 'Created', 201, {'location': '/photographer/' + str(display_name)}
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.NetworkTimeout) as e:
        return 'Mongo unavailable', 503

