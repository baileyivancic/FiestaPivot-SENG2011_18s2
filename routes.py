import flask_login
from flask import Flask, redirect, render_template, request, url_for, flash, request, Response
from flask_login import LoginManager,login_user, current_user, login_required, logout_user, UserMixin
import json
import sys
import copy
import datetime
from database import Database
from server import app, login_manager
from functions import bubbleDateAds, bubblePriceAds

class Controller:
	def __init__(self):
		self.database = Database()

	def register_user(self, username, password, email, city, state):
		return self.database.register_user(username, password, email, city, state)

	def isValidUser(self, username, password):
		return self.database.isValidUser(username, password)

	def get_name(self, email):
		return self.database.get_name(email)

	def postAd(self, email, title, price, city, state, descr, date, start_time, end_time, alcohol, noPeople):
		return self.database.create_ad(email, title, price, city, state, descr, date, start_time, end_time, alcohol, noPeople)
	
	def postBid(self, adID, adName, userID, price, comment, status):
		return self.database.create_bid(adID, adName, userID, price, comment, status)
	
	def fetch_ads(self):
		return self.database.fetch_ads()

	def find_user_ads(self, ad_id):
		return self.database.find_user_ads(ad_id)

	def find_user_bids(self, bid_id):
		return self.database.find_user_bids(bid_id)
	
	def get_city(self, id):
		return self.database.get_city(id)
	
	def get_state(self, id):
		return self.database.get_state(id)
	
	def get_Title(self, id):
		return self.database.getTitle(id)

	def delete_ad(self, ad_id):
		return self.database.delete_ad(ad_id)

	def delete_bid(self, bid_id):
		return self.database.delete_bid(bid_id)

	def getBids(self, adID):
		return self.database.getBids(adID)
	
	def getAdBid(self, bidID):
		return self.database.getAdIDFromBid(bidID)

	def setBidStatus(self, status, bidID):
		return self.database.setBidStatus(status, bidID)

	def setAdStatus(self, status, adID):
		return self.database.setAdStatus(status, adID)
	
	def get_about(self, email):
		return self.database.get_about(email)

	def get_phone(self, email):
		return self.database.get_phone(email)
	
	def get_adsPosted(self, email):
		return self.database.get_adsPosted(email)
	
	def get_bidsPosted(self, email):
		return self.database.get_bidsPosted(email)
	
	def get_rating(self, email):
		return self.database.get_rating(email)

	def getInfo(self, ID):
		user = []
		email = current_user.get_id()

		user.append(email)
		user.append(self.get_city(email))
		user.append(self.get_state(email))
		user.append(self.get_about(email))
		user.append(self.get_phone(email))
		user.append(self.get_adsPosted(email))
		user.append(self.get_bidsPosted(email))
		user.append(self.get_rating(email))
		return user
	
	# Determines if the ad has a winning bid
	# Returns 1 for yes, 0 for no
	def findWinning(self, adID):
		bids = self.getBids(adID)
		flag = 0
		for bid in bids:
			if (bid[6] == "PROGRESS"):
				flag = 1
				break
		
		return flag

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
login_manager.login_message = ""

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

	name = control.database.get_name( current_user.get_id() )

	print(current_user.get_id())
	return render_template("index.html", user=current_user.get_id(), name=name)

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
		about = request.form["about"]
		if (about == ""):
			about = "I just love food!"
		if password != passwordConfirm:
			valid = 3
		elif email != emailConfirm:
			valid = 4
		else:
			valid = control.register_user(user, password, email, city, state)
		if valid == 1:
			login_user(User(email), remember= False)
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
	state = control.get_state(current_user.get_id())
	city = control.get_city(current_user.get_id())

	# Submit putton pressed
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
		alcohol = request.form['alcohol'].strip()
		noPeople = request.form['noPeople'].strip()

		print(title)

		if control.postAd(email, title, price, city, state, descr, date, start_time, end_time, alcohol, noPeople):
			print("WENT IN HERE")
			return redirect("/account")
	return render_template("post.html", state=state, city=city)
	

@app.route('/account',  methods=["GET", "POST"])
@login_required
def account():
	ads = control.find_user_ads( current_user.get_id() )
	newAds = bubbleDateAds(ads)
	bids = control.find_user_bids( current_user.get_id() )
	name = control.database.get_name( current_user.get_id() )
	
	# Get bids associated with each ad
	bidsOrdered=[]
	for ad in ads:
		# print( control.getBids(ad[0]) )
		for bid in control.getBids(ad[0]):
			bidsOrdered.append( bid )

	info = control.getInfo(current_user.get_id())

	x = 0
	while x < 8:
		print("info is " + info[x])
		x+=1
	return render_template("user-dashboard.html", ads=newAds, bids=bids, name=name, bidsOrdered=bidsOrdered, info=info, edit=False)

@app.route('/delete-ad',  methods=["GET", "POST"])
@login_required
def delete_ad():
	# print(f"delete: form: {request.form}")
	ad_id = request.form["id"]
		
	control.delete_ad(ad_id)
	return redirect("/account")

@app.route('/delete-bid',  methods=["POST"])
@login_required
def delete_bid():
	# print(f"delete: form: {request.form}")
	bid_id = request.form["id"]
		
	control.delete_bid(bid_id)
	return redirect("/account")

@app.route('/choose-bid',  methods=["POST"])
@login_required
def choose_bid():
	# print(f"delete: form: {request.form}")
	bidID = request.form["id"]
	adID = control.getAdBid(bidID)

	# Set Status of chosen ad to PROGRESS
	control.setAdStatus("PROGRESS", adID)

	# Set status of other bids to DECLINED	
	bids = control.getBids(adID)
	for bid in bids:
		control.setBidStatus("DECLINED", bid[0])

	# Set status of chosen bid to ACCEPTED
	control.setBidStatus("ACCEPTED", bidID)	

	return redirect("/account")


@app.route('/about',  methods=["GET", "POST"])
def about():
	if request.method == "POST":
		print("POST")

	name = control.database.get_name( current_user.get_id() )

	print(current_user.get_id())
	return render_template("about.html", user=current_user.get_id(), name=name)

@app.route('/search', methods=["GET", "POST"])
@login_required
def search():
	ads = control.fetch_ads()
	name = control.get_name( current_user.get_id() )
	newAds = bubbleDateAds(ads)

	# Changing sorting of ads based on user choice
	if request.method == "SORT":
		sort = request.form['sortSelect']
		if sort == "dateAsc":
			newAds = bubbleDateAds(ads)
			print("Date asc ")

		elif sort == "dateDes":
			newAds = list(reversed(bubbleDateAds(ads)))
			print("Date des ")
		
		elif sort == "priceAsc":
			newAds = bubblePriceAds(ads)
			print("Price asc ")
		
		elif sort == "priceDes":
			newAds = list(reversed(bubblePriceAds(ads)))
			print("Price des")
	
	print(newAds)
	
	return render_template("search.html", ads=newAds, name=name)

# Creating bid from user input after searching
@app.route('/bid-send', methods=['GET', 'POST'])
@login_required
def bidSend():
	db = Database()

    # Grab information from request
	userID = current_user.get_id()
	price = request.form['priceInput'].strip()
	comment = request.form['commentInput'].strip()
	adID = request.form['adID'].strip()
	adName = db.getTitle(adID)
	status = "PENDING"

	# Put data in db
	control.postBid(adID, adName, userID, price, comment, status)
	return search()


# def checkAds():
# 	ads = control.fetch_ads()
# 	for ad in ads:
# 		adDate = ad[8]
# 		currDate = datetime.datetime.now().date()
# 		adID = ad[0]
# 		adTime = ad[9]
		
# 		# Check if the bid has expired
# 		if (adDate > currDate): # Date has been passed,
# 			if (findWinning(adID) == 0): # Ad does not have a winning bid associated with it
# 				control.setAdStatus("EXPIRED", asID)
# 			else:
# 				control.setAdStatus("COMPLETED", adID)


# 		if (adDate == currDate): # Check if the starting time has been reached
# 			pass

		
# TODO:
# - Change schema to say adID and bidID and all that stuff
# - put date on ACCEPTED bids

#Done 
# - Deleting ad that user has created 
# - Deleting bid user has created 
# - Showing all bids registered for current ad 