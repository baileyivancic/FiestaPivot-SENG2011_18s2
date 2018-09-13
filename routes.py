import flask_login
from flask import Flask, redirect, render_template, request, url_for, flash, request, Response
from flask_login import UserMixin
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
import json
from database import Database
from server import app, login_manager

class Controller:
    def __init__(self):
        self.database = Database()
        self.database.first_run()

    def register_user(self, username, password):
        return self.database.register_user(username, password)

    def isValidUser(self, username, password):
        return self.database.isValidUser(username, password)


class User(UserMixin):
	def __init__(self, id):
		self.id = id

	def get_id(self):
		return self.id

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

control = Controller()

def check_password(user_id, password):
	if control.isValidUser(user_id, password):
		user = User(user_id)
		login_user(user)
		return True
	return False

def get_user(user_id):

	return User(user_id)

@login_manager.user_loader
def load_user(user_id):
	# get user information from db
	user = get_user(user_id)
	return user

login_manager.login_view = "login"
login_manager.login_message = "Welcome"

@app.route('/',  methods=["GET", "POST"])
def landing_page():
    return render_template("register.html")