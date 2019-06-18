#!/usr/bin/env python3

import logging
import json

import connexion
from connexion import NoContent

from flask import jsonify
import json

def say_hello():
    return {'message': 'hello'}

def say_greeting(firstname):
    return {'message': 'greeting to '+firstname}
