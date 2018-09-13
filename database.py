import os
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

class Database(object):

    def __init__(self):
        db = self.get_db()

        with current_app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))

    def get_db(self):
        if 'db' not in g:
            g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row

        return g.db


    def close_db(self, e=None):
        db = g.pop('db', None)

        if db is not None:
            db.close()

    def first_run(self):
        pass

    def register_user(self, username, password):
        pass

    def isValidUser(self, username, password):
        pass