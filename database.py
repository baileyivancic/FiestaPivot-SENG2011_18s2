import os
import sqlite3

class Database(object):

    def __init__(self):
        db = self.get_db()

        with open("schema.sql") as f:
            db.executescript(f.read())

        db.close()

    def get_db(self):
        db = sqlite3.connect('database.db')
        return db

    def first_run(self):
        pass

    def register_user(self, username, password):
        pass

    def isValidUser(self, username, password):
        pass