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

	def register_user(self, email, user, password, city, state, rating, adsPosted, bidsPosted, about, phone):
		print("In register phone is ")
		print(phone)
		return self.database.register_user(email, user, password, city, state, rating, adsPosted, bidsPosted, about, phone)

	def isValidUser(self, username, password):
		return self.database.isValidUser(username, password)

	def get_name(self, email):
		return self.database.get_name(email)

	def postAd(self, email, title, price, city, state, descr, date, start_time, end_time, alcohol, noPeople):
		return self.database.create_ad(email, title, price, city, state, descr, date, start_time, end_time, alcohol, noPeople)
	
	def postBid(self, adID, adName, userID, price, comment, status, oPrice, date):
		return self.database.create_bid(adID, adName, userID, price, comment, status, oPrice, date)
	
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
	
	def getAdPrice(self, adID):
		return self.database.getAdPrice(adID)
	
	def setWinning(self, adID, bidID):
		return self.database.setWinning(adID, bidID)


	# Determines if the ad has a winning bid
	# Returns 1 for yes, 0 for no
	def findWinning(self, adID):
		bids = self.getBids(adID)
		flag = 0
		for bid in bids:
			if (bid[6] == "ACCEPTED"):
				flag = 1
				break
		
		return flag
	
	def fetch_bids(self):
		return self.database.getAllBids()

	def getAd(self, adID):
		return self.database.getAd(adID)

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
	checkAds() # Automatic ad expiry
	checkBids() # Automatic bid status change
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
		state = request.form["state"].strip()
		about = request.form["about"].strip()
		phone = request.form["phoneNo"].strip()

		print("Phone is " + phone)

		if (about == ""):
			about = "I just love food!"

		if password != passwordConfirm:
			valid = 3
		elif email != emailConfirm:
			valid = 4
		else:
			valid = control.register_user(email, user, password, city, state, 0, 0, 0, about, phone)
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
	name = control.get_name(current_user.get_id())

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
			return redirect("/account")
	return render_template("post.html", state=state, city=city, name=name)
	

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
		print(info[x])
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
	control.setWinning(adID, bidID)

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
	email = current_user.get_id()
	newAds = bubbleDateAds(ads)

	# TODO - put different sorted lists into a big list, and pass that into html page

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
	
	return render_template("search.html", ads=newAds, name=name, email=email)

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
	oPrice = int(control.getAdPrice(adID))
	date = datetime.datetime.today().strftime('%Y-%m-%d')

	# Put data in db
	control.postBid(adID, adName, userID, price, comment, status, oPrice, date)
	return search()

# Checks all ads in the system to see if they have been completed, or if they are expired
def checkAds():
	ads = control.fetch_ads()
	for ad in ads:
		adDate = ad[8]
		currDate = datetime.datetime.today().strftime('%Y-%m-%d')
		adID = ad[0]
		adTime = ad[9]
		
		# Check if the bid has expired
		if (adDate < currDate): # Date has been passed
			if (control.findWinning(adID) == 0): # Ad does not have a winning bid associated with it
				control.setAdStatus("EXPIRED", adID)
			else:
				control.setAdStatus("COMPLETED", adID)
				# find winning bid and set that to completed

		# if (adDate == currDate): # Check if the starting time has been reached
		# 	pass

# Checks all bids in the system to update status
def checkBids():
	bids = control.fetch_bids()

	# # Go through bids and check ad status
	for bid in bids:
		print("Bod is -")
		print(bid)
		ad = control.getAd(bid[1])
		if (ad == None):
			control.setBidStatus("AD DELETED", bid[0])
		else:
			if (ad[7] == "EXPIRED"):
				control.setBidStatus("DECLINED", bid[0])
			elif (ad[7] == "PROGRESS" or ad[7] == "COMPLETED"):
				if (ad[13] == bid[0]):
					control.setBidStatus("ACCEPTED", bid[0])
				else:
					control.setBidStatus("DECLINED", bid[0])
			elif (ad[7] == "ACTIVE"):
				control.setBidStatus("PENDING", bid[0])