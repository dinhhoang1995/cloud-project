import pytest
import connexion
import json
from bson import json_util
import logging

#logging.basicConfig(level=logging.DEBUG)

@pytest.mark.usefixtures("clearPhotographers")
@pytest.mark.usefixtures("initDB")
class TestClass(object):

    data1 = {'display_name': 'rdoisneau',
             'first_name': 'Robert',
             'last_name': 'Doisneau',
             'interests': ['street']
    }

    data2 = {'display_name': 'hsentucq',
             'first_name': 'Hervé',
             'last_name': 'Sentucq',
             'interests': ['landscape']
    }

    data3 = {'display_name': 'rdoisneau',
             'first_name': 'Robert',
             'last_name': 'Doisneau',
             'interests': ['coca']
    }

    headers_content = {'Content-Type': 'application/json'}
    headers_accept  = {'Accept': 'application/json'}

    @staticmethod
    def test_post_once(client):
        response = client.post('/photographers', headers=TestClass.headers_content,
                               data=json.dumps(TestClass.data1))
        assert response.headers['Location']
        assert response.status_code == 201

    @staticmethod
    def test_post_twice(client):
        response1 = client.post('/photographers', headers=TestClass.headers_content,
                               data=json.dumps(TestClass.data1))
        assert response1.status_code == 201
        response2 = client.post('/photographers', headers=TestClass.headers_content,
                               data=json.dumps(TestClass.data1))
        assert response2.status_code == 409

    @staticmethod
    def test_post_delete_post(client):
        response1 = client.post('/photographers', headers=TestClass.headers_content,
                               data=json.dumps(TestClass.data1))
        assert response1.status_code == 201

        response2 = client.delete(response1.headers['Location'])
        assert response2.status_code == 204        

        response3 = client.post('/photographers', headers=TestClass.headers_content,
                               data=json.dumps(TestClass.data1))
        assert response3.status_code == 201

    @staticmethod
    def test_post_put(client):
        response1 = client.post('/photographers', headers=TestClass.headers_content,
                                data=json.dumps(TestClass.data1))
        assert response1.status_code == 201

        response2 = client.put(response1.headers['Location'], headers=TestClass.headers_content,
                               data=json.dumps(TestClass.data3))
        assert response2.status_code == 201