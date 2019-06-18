#!/usr/bin/env python3

import logging
import connexion
from connexion import NoContent

logging.basicConfig(level=logging.DEBUG)

app = connexion.FlaskApp(__name__)

app.add_api('hello_service.yml', validate_responses=True)

# from http://coderobot.downley.net/swagger-driven-testing-in-python.html
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':
    app.run(port=8090)
