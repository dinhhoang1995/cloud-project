#!/usr/bin/env python3

import logging
import json

import connexion
from connexion import NoContent
from photo import Photo
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
def mongo_add(name, photo):
    ph = Photo(title='title', location='location', author=name, comment='comment', tags=['tags'], photo=photo).save()
    return ph

@robustify.retry_mongo
def mongo_get_photos(name, offset, limit):
    list_ph = Photo.objects(author=name).order_by('id').skip(offset).limit(limit)
    if list_ph.count(with_limit_and_skip = False) > (offset + limit):
        has_more = True
    else:
        has_more = False

    return (has_more, list_ph)

@robustify.retry_mongo
def mongo_get_photo_by_id(name, photo_id):
    ph = Photo.objects(id=ObjectId(photo_id), author=name).get()
    return ph

@robustify.retry_mongo
def mongo_delete_photo_by_id(name, photo_id):
    try:
        ph = Photo.objects(id=ObjectId(photo_id), author=name).get()
    except (Photo.DoesNotExist,
            Photo.MultipleObjectsReturned):
        return False
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.NetworkTimeout) as e:
        raise 
    ph.delete()
    return True

@robustify.retry_mongo
def mongo_get_attributes_by_id(name, photo_id):
    ph = Photo.objects(id=ObjectId(photo_id), author=name).get()
    attributes = json.loads(json.dumps({'title':ph.title,
                             'location':ph.location,
                             'author':ph.author,
                             'comment':ph.comment,
                             'tags':ph.tags}))
    return attributes

@robustify.retry_mongo
def mongo_set_attributes_by_id(name, photo_id, body):
    attributes = body
    ph = Photo.objects(id=ObjectId(photo_id), author=name).update(title=attributes['title'],
                                                                  location=attributes['location'],
                                                                  comment=attributes['comment'],
                                                                  tags=attributes['tags'])
    return ph