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
	
	def postBid(self, adID, userID, price, comment):
		return self.database.create_bid(adID, userID, price, comment)
	
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
@login_required
def default():
	if request.method == "POST":
		if request.form['submit-but'] == "dash":
			return render_template("user-dashboard.html")
		elif reques.form['submit-but'] == "search":
			return render_template("search.html")
		#keywords = request.form['indexInput']
		return searchI(keywords)
	return render_template("index.html")

@app.route('/login',  methods=["GET", "POST"])
def login():
	if request.method == "POST":
		#print("POST")
		email = request.form["email"].strip()
		password = request.form["password"].strip()
		valid = control.isValidUser(email, password)
		if valid == True:
			login_user(User(email), remember= False)
			return redirect("/")
		else:
			return render_template("login.html")
	return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		user = request.form["username"].strip()
		password = request.form["password"].strip()
		email = request.form["email"].strip()
		city = request.form["city"].strip()
		state = request.form["state"] 
		#print(f"register Attempt: U:{user}\nP:{password}\nE:{email}\nC:{city}\nS:{state}\n")
		valid = control.register_user(user, password, email, city, state)
		if valid == True:
			login_user(User(user), remember= False)
			return redirect("/")
		else:
			return render_template("register.html", response=0)
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
			pass
		# print(f"for user {name}:\n")
		# print(f"form: \nN:{name}\nT:{title}\nE:{email}\nC:{city}\nS:{state}\nDes:{descr}\nDa:{date}\nST:{start_time}\nET:{end_time}\n")
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
def search():
	ads = control.fetch_ads()

# Order as most recent
	newAds = bubbleAds(ads)
	return render_template("search.html", ads=newAds)

# Creating bid from user input after searching
@app.route('/bid-send', methods=['GET', 'POST'])
def bidSend():
    # Grab information from request, and put in db
	userID = current_user.get_id()
	price = request.form['priceInput'].strip()
	comment = request.form['commentInput'].strip()
	adID = request.form['adID'].strip()
	print("user os " + userID)
	print("price is " + price)
	print("desc " + comment)
	print("adID is " + adID)

	control.postBid(adID, userID, price, comment)

	return search()