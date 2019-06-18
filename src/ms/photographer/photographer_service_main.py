#!/usr/bin/env python3

import logging
import connexion
from connexion import NoContent
from mongoengine import connect

logging.basicConfig(level=logging.DEBUG)
import warnings
warnings.simplefilter('always')

app = connexion.FlaskApp(__name__)

app.add_api('photographer_service.yml', validate_responses=True)

# connect("photographers", host="172.17.0.2")
# connect("photographers", host="mongo-service")
connect(host="mongodb://siteRootAdmin:passw0rd@mongo1:27017,mongo2:27017,mongo3:27017/photographers?authSource=admin&replicaSet=therep")

# from http://coderobot.downley.net/swagger-driven-testing-in-python.html
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':
    app.run(port=8090)
