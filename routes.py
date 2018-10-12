import flask_login
from flask import Flask, redirect, render_template, request, url_for, flash, request, Response
from flask_login import UserMixin
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
import json
import sys
import copy
from database import Database
from server import app, login_manager
from functions import bubbleAds

class Controller:
	def __init__(self):
		self.database = Database()

	def register_user(self, username, password, email, city, state):
		return self.database.register_user(username, password, email, city, state)

	def isValidUser(self, username, password):
		return self.database.isValidUser(username, password)

	def get_name(self, email):
		return self.database.get_name(email)

	def postAd(self, email, title, price, city, state, descr, date, start_time, end_time):
		return self.database.create_ad(email, title, price, city, state, descr, date, start_time, end_time)
	
	def postBid(self, adID, adName, userID, price, comment):
		return self.database.create_bid(adID, adName, userID, price, comment)
	
	def fetch_ads(self):
		return self.database.fetch_ads()

class User(UserMixin):
	def __init__(self, id):
		self.email = id

	def get_id(self):
		return self.email

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

@app.route("/logout",  methods=["GET", "POST"])
@login_required
def logout():
	logout_user()
	return redirect("/login")

# Default page, index page
@app.route('/',  methods=["GET", "POST"])
def default():
	if request.method == "POST":
		if request.form['submit-but'] == "dash":
			return render_template("user-dashboard.html")
		elif request.form['submit-but'] == "search":
			return render_template("search.html")
		#keywords = request.form['indexInput']
	return render_template("index.html")

@app.route('/login',  methods=["GET", "POST"])
def login():
	error = None
	if request.method == "POST":
		email = request.form["email"].strip()
		password = request.form["password"].strip()
		valid = control.isValidUser(email, password)
		if valid == True:
			login_user(User(email), remember= False)
			flash('You were successfully logged in')
			return account()
		else:
			error = 'Invalid username or password. Please try again!'
	return render_template("login.html", error=error)

@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		user = request.form["username"].strip()
		password = request.form["password"].strip()
		passwordConfirm = request.form['passwordConfirm'].strip()
		email = request.form["email"].strip()
		emailConfirm = request.form['emailConfirm'].strip()
		city = request.form["city"].strip()
		state = request.form["state"] 
		if password != passwordConfirm:
			valid = 3
		elif email != emailConfirm:
			valid = 4
		else:
			valid = control.register_user(user, password, email, city, state)
		if valid == 1:
			login_user(User(user), remember= False)
			flash("Successfully created account!")
			return account()
		elif valid == 0:
			error = "Please try again, there is already a user with this email addresss"
			return render_template("register.html", error=error)
		elif valid == 3:
			error = "Passwords do not match, please try again"
			return render_template("register.html", error=error)
		elif valid == 4:
			error = "Emails do not match, please try again"
			return render_template("register.html", error=error)
	return render_template("register.html")

@app.route('/post-ad', methods=["GET", "POST"])
@login_required
def post():
	if request.method == "POST":
		name = control.get_name( current_user.get_id() )
		email = current_user.get_id()
		title = request.form["title"].strip()
		city = request.form["city"].strip()
		state = request.form["state"].strip()
		price = request.form["price"].strip()
		descr = request.form["descr"].strip()
		date = request.form["date"].strip()
		start_time = request.form["start-time"].strip()
		end_time = request.form["end-time"].strip()

		if control.postAd(email, title, price, city, state, descr, date, start_time, end_time):
			return account()
	return render_template("post.html")
	

@app.route('/account',  methods=["GET", "POST"])
@login_required
def account():
	db = Database()
	ads = db.find_user_ads( current_user.get_id() )
	newAds = bubbleAds(ads)
	bids = db.find_user_bids( current_user.get_id() )
	return render_template("user-dashboard.html", ads=newAds, bids=bids)

@app.route('/about',  methods=["GET", "POST"])
def about():
	if request.method == "POST":
		print("POST")
	return render_template("about.html")

@app.route('/search', methods=["GET", "POST"])
@login_required
def search():
	ads = control.fetch_ads()

# Order as most recent
	newAds = bubbleAds(ads)
	return render_template("search.html", ads=newAds)

# Creating bid from user input after searching
@app.route('/bid-send', methods=['GET', 'POST'])
def bidSend():
	db=Database()

    # Grab information from request
	userID = current_user.get_id()
	price = request.form['priceInput'].strip()
	comment = request.form['commentInput'].strip()
	adID = request.form['adID'].strip()
	adName = db.getTitle(adID)

	# Put data in db
	control.postBid(adID, adName, userID, price, comment)
	return search()


# TODO:
# - Deleting ad that user has created 
# - Editing ad that user has created (Nabil)
# - Deleting bid user has created 
# - Showing all bids registered for current ad 
# - Change schema to say adID and bidID and all that stuff
# - shouldn't be able to make a bid for your own ad in the user-dashboard (Nabil)