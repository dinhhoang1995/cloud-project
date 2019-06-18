#!/usr/bin/env python3

import logging
import json

import connexion
from connexion import NoContent
from photographer import Photographer
from mongoengine import *
import socket
import pymongo

from bson.objectid import ObjectId
from bson import json_util
from bson.errors import InvalidId

from flask import jsonify
import json
import flask
import robustify

logging.basicConfig(level=logging.DEBUG)

@robustify.retry_mongo
def mongo_check(display_name):
    count = Photographer.objects(display_name=display_name).count()
    return count

@robustify.retry_mongo
def mongo_add(display_name, first_name, last_name, interests):
    ph = Photographer(display_name = display_name,
                      first_name = first_name,
                      last_name = last_name,
                      interests = interests).save()
    return ph

@robustify.retry_mongo
def mongo_get_photographers(offset, limit):
    qs = Photographer.objects.order_by('id').skip(offset).limit(limit)
    if qs.count(with_limit_and_skip = False) > (offset + limit):
        has_more = True
    else:
        has_more = False

    return (has_more, qs)

@robustify.retry_mongo
def mongo_get_photographer_by_id(photographer_id):
    ph = Photographer.objects(id=ObjectId(photographer_id)).get()
    return ph

@robustify.retry_mongo
def mongo_get_photographer_by_name(name):
    ph = Photographer.objects(display_name=name).get()
    return ph

@robustify.retry_mongo
def mongo_delete_photographer_by_name(name):
    try:
        ph = Photographer.objects(display_name=name).get()
    except (Photographer.DoesNotExist,
            Photographer.MultipleObjectsReturned):
        return False
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.NetworkTimeout) as e:
        raise 
    ph.delete()
    return True

@robustify.retry_mongo
def mongo_update_photographers_by_name(display_name, first_name, last_name, interests):
    ph = Photographer.objects(display_name = display_name).update(first_name = first_name, last_name = last_name, interests = interests)
    return ph