import json
import datetime
import os
import tempfile
import sqlite3

import pytest

from app import start


@pytest.fixture
def client():
    db_fd, start.app.config['DATABASE'] = tempfile.mkstemp()
    start.app.config['TESTING'] = True

    with start.app.test_client() as client:
        with start.app.app_context():
            start.init_db()
        yield client

    os.close(db_fd)
    os.unlink(start.app.config['DATABASE'])


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'Hello, World!' in rv.data


def test_insert(client):
    """Test adding in a new request"""
    email = 'test@tester.com'
    title = 'Ulysses'

    data = json.dumps({'email': email, 'title': title})
    response = client.post('/request', data=data, content_type='application/json')

    assert response.content_type == 'application/json'

    response_json = response.json
    assert type(response_json['id']) == int
    assert response_json['title'] == 'Ulysses'
    assert type(response_json['dt']) == str
    assert response_json['email'] == 'test@tester.com'


def test_valid_email(client):
    """Test adding in a new request"""
    title = 'Ulysses'
    data = json.dumps({'email': 'test@testercom', 'title': title})
    response = client.post('/request', data=data, content_type='application/json')
    assert response.json == {'Message': 'Not valid email'}


def test_get_unknown(client):
    response = client.get('/request/2')

    assert response.content_type == 'application/json'
    assert response.json == {'Message': 'Unknown ID'}

#
# def test_get(client):
#     dt = datetime.datetime.now()
#     title = 'test_tite'
#     email = 'test@testing.com'
#
#     conn = sqlite3.connect("database/flask_library.db")
#     c = conn.cursor()
#     r = c.execute('INSERT INTO bookrequests (dt, title, email) VALUES (?, ?, ?)', [dt, title, email])
#     conn.commit()
#     print(r)
#     c.close()
#
#     response = client.get('/request/1')
#
#     assert response.content_type == 'application/json'
#     assert response.json == {'Message': 'Unknown ID'}
