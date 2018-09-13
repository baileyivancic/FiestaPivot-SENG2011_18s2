import os
import sqlite3

class Database(object):

    def __init__(self):
        db = self.get_db()

        with open("schema.sql") as f:
            db.executescript(f.read())

        self.close(db)

    def get_db(self):
        db = sqlite3.connect('database.db')
        return db

    def close(self, db):
        db.commit()
        db.close()

    def first_run(self):
        pass

    def register_user(self, username, password, email, city, state):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT EXISTS(SELECT 1 FROM accounts WHERE username=? AND password=?)", (username, password))
        temp =  cursor.fetchone()

        print("result from db ", temp)
        if temp != (0, ):
            # there is already a user using this user name
            db.commit()
            db.close()
            return 0
        else :
            cursor.execute('''INSERT INTO accounts (username, password, email, city, state) VALUES (?, ?, ?, ?, ?)''',(username, password, email, city, state))
            db.commit()
            db.close()
            return 1



    def isValidUser(self, email, password):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT EXISTS(SELECT 1 FROM accounts WHERE email=? AND password=?)", (email, password, ))
        temp =  cursor.fetchone()

        isValid = False

        if temp != (0, ):
            # there is already a user using this user name
            isValid = True


        self.close(db)

        return isValid

    def get_name(self, email):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT EXISTS(SELECT 1 FROM accounts WHERE email=?)", (email, ))
        temp = cursor.fetchone()

        isValid = False

        if temp != (0, ):
            # there is already a user using this user name
            isValid = True


        self.close(db)

        return isValid
