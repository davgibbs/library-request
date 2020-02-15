import sqlite3
import os
import datetime

from flask import Flask, g, request, jsonify, current_app

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, "../database/flask_library.db"),
    DEBUG=True
))


def init_db():
    db = get_db()

    with current_app.open_resource('../database/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def get_db():
    """
    Opens a new database connection if there is none yet for the current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def hello_world():
    return 'Hello, World!'


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def _get_bookrequest_title_email(title, email):
    db = get_db()
    db.row_factory = dict_factory
    cur = db.execute('SELECT * FROM bookrequests where title=? and email=?', [title, email])
    d = cur.fetchone()
    return d


def _get_bookrequests():
    db = get_db()
    db.row_factory = dict_factory
    cur = db.execute('SELECT * FROM bookrequests')
    d = cur.fetchall()

    return jsonify(d)


@app.route('/request', methods=['POST', 'GET'])
def request_base():
    if request.method == 'GET':
        d = _get_bookrequests()
        return d

    req_data = request.get_json()
    email = req_data['email']
    title = req_data['title']
    dt = datetime.datetime.now()

    db = get_db()
    db.execute('INSERT INTO bookrequests (dt, title, email) VALUES (?, ?, ?)',
               [dt, title, email])
    db.commit()

    return _get_bookrequest_title_email(title, email)


def _get_bookrequest_id(request_id):
    db = get_db()
    db.row_factory = dict_factory
    cur = db.execute('SELECT * FROM bookrequests where id = ?', (request_id,))
    d = cur.fetchone()
    return d


def _delete_bookrequest_id(request_id):
    db = get_db()
    db.row_factory = dict_factory
    db.execute('DELETE FROM bookrequests where id = ?', (request_id,))
    db.commit()


@app.route('/request/<request_id>', methods=['GET', 'DELETE'])
def request_id(request_id):
    if request.method == 'DELETE':
        _delete_bookrequest_id(request_id)
        return {'Message': 'Success'}

    d = _get_bookrequest_id(request_id)
    if not d:
        return {'Message': 'Unknown ID'}
    return d


if __name__ == "__main__":
    app.run()
