import os
import sqlite3

class Database(object):

#   Common functions
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

# Login db functions
    def register_user(self, email, user, password, city, state, rating, adsPosted, bidsPosted, about, phone):
        db = self.get_db()
        cursor = db.cursor()

        print("In db phone is ")
        print(phone)

        cursor.execute("SELECT EXISTS(SELECT 1 FROM accounts WHERE email=?)", (email,))
        temp =  cursor.fetchone()
        if temp != (0, ):
            # there is already a user using this user name
            db.commit()
            db.close()
            return 0
        else:
            cursor.execute('''INSERT INTO accounts (email, username, password, city, state, rating, adsPosted, bidsPosted, about, phoneNo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',(email, user, password, city, state, rating, adsPosted, bidsPosted, about, str(phone)))
            db.commit()
            db.close()
            return 1

    def isValidUser(self, email, password):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT EXISTS(SELECT 1 FROM accounts WHERE email=? AND password=?)", (email, password, ))
        temp =  cursor.fetchone()
        isValid = False

        # there is already a user using this user name
        if temp != (0, ):
            isValid = True
        self.close(db)

        return isValid

    def get_name(self, email):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT username FROM accounts WHERE email=?", (email, ))
        temp = cursor.fetchone()

        if temp == False:
            return False

        self.close(db)
        return temp

    def get_state(self, email):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT state FROM accounts WHERE email=?", (email, ))
        temp = cursor.fetchone()

        if temp == False:
            return False

        self.close(db)
        return temp[0]

    def get_city(self, email):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT city FROM accounts WHERE email=?", (email, ))
        temp = cursor.fetchone()

        if temp == False:
            return False

        self.close(db)
        return temp[0]
    
    def get_about(self, email):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT about FROM accounts WHERE email=?", (email, ))
        temp = cursor.fetchone()

        if temp == False:
            return False

        self.close(db)
        return temp[0]

    def get_phone(self, email):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT phoneNo FROM accounts WHERE email=?", (email, ))
        temp = cursor.fetchone()

        if temp == False:
            return False

        self.close(db)
        return temp[0]
    
    def get_adsPosted(self, email):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT adsPosted FROM accounts WHERE email=?", (email, ))
        temp = cursor.fetchone()

        if temp == False:
            return False

        self.close(db)
        return temp[0]

    def get_bidsPosted(self, email):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT bidsPosted FROM accounts WHERE email=?", (email, ))
        temp = cursor.fetchone()

        if temp == False:
            return False

        self.close(db)
        return temp[0]
    
    def get_rating(self, email):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT rating FROM accounts WHERE email=?", (email, ))
        temp = cursor.fetchone()

        if temp == False:
            return False

        self.close(db)
        return temp[0]

# Advertisement db functions
    def create_ad(self, userEmail, title, price, city, state, descr, date, start_time, end_time, alcohol, noPeople):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute('''INSERT INTO ads (userEmail, title, price, city, state, descr, status, date, start_time, end_time, alcohol, noPeople) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',(userEmail, title, price, city, state, descr, "ACTIVE", date, start_time, end_time, alcohol, noPeople))
        
        self.close(db)
        return True

    def delete_ad(self, ad_id):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("DELETE FROM ads WHERE ID=?", ad_id)

        self.close(db)
        return

    def delete_bid(self, bid_id):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("DELETE FROM bids WHERE ID=?", bid_id)

        self.close(db)
        return
    
    #UNTESTED
    def updateActive_ad(self, adID, newActive):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT EXISTS(SELECT 1 FROM ads WHERE adID=?)", (adID))
        temp =  cursor.fetchone()
        
        if temp == 0:
            # Could not find ad assocoated with this adID
            print("Something went wrong, ad does not exist\n")
            db.commit()
            db.close()
            return 0
        else :
            cursor.execute('''INSERT INTO ads (active) VALUES (?)''',(newActive))
            db.commit()
            db.close()
            return 1

# Bid db functions
    #UNTESTED
    def create_bid(self, adID, adName, userEmail, price, comment, status, oPrice, date):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT EXISTS(SELECT 1 FROM bids WHERE adID=? AND userEmail=?)", (adID, userEmail))
        temp = cursor.fetchone()

        cursor.execute('''INSERT INTO bids (adID, adName, userEmail, price, comment, status, oPrice, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',(adID, adName, userEmail, price, comment, status, oPrice, date))
        db.commit()
        db.close()
        return 1
    
    #UNTESTED
    def updatePrice_bid(self, adID, userID, newPrice):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT EXISTS(SELECT 1 FROM bids WHERE adID=? AND userID=?)", (adID, userID))
        temp =  cursor.fetchone()
        
        if temp == (0, ):
            # Could not find userID or adID
            print("Something went wrong, could not access correct user or ad\n")
            db.commit()
            db.close()
            return 0
        else :
            cursor.execute('''INSERT INTO bids (price) VALUES (?)''',(newPrice))
            db.commit()
            db.close()
            return 1

    #UNTESTED
    def updateComment_bid(self, adID, userID, newComment):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT EXISTS(SELECT 1 FROM bids WHERE adID=? AND userID=?)", (adID, userID))
        temp =  cursor.fetchone()
        
        if temp == (0, ): #TODO - CHECK THIS
            # Could not find userID or adID
            print("Something went wrong, could not access correct user or ad\n")
            db.commit()
            db.close()
            return 0
        else :
            cursor.execute('''INSERT INTO bids (comment) VALUES (?)''',(newComment))
            db.commit()
            db.close()
            return 1

    # Gets all ads that are currently in db
    def fetch_ads(self):
        db = self.get_db()
        cursor = db.cursor()

        ads = cursor.execute("SELECT * FROM ads").fetchall()

        self.close(db)
        return ads

    # Finds all ads for logged in user
    def find_user_ads(self, email):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM ads WHERE userEmail=?", (email, ))
        temp = cursor.fetchall()

        if temp == False:
            return False

        self.close(db)
        return temp
    
    # Finds all bids for logged in user
    def find_user_bids(self, email):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM bids WHERE userEmail=?", (email, ))
        temp = cursor.fetchall()

        self.close(db)
        return temp
    
    # Function to get ad title from the id given
    def getTitle(self, adID):
        db = self.get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM ads WHERE ID=?", (adID, ))
        temp = cursor.fetchone()

        self.close(db)
        return temp[2]
    
    # Returns bids for a given adID
    def getBids(self, adID):
        db = self.get_db()
        cursor=db.cursor()

        cursor.execute("SELECT * FROM bids WHERE adID=?", (adID, ))
        temp = cursor.fetchall()

        self.close(db)
        return temp

    # Gets ad from bid id
    def getAdIDFromBid(self, bidID):
        db = self.get_db()
        cursor=db.cursor()

        cursor.execute("SELECT * FROM bids WHERE ID=?", (bidID, ))
        temp = cursor.fetchone()

        self.close(db)
        return temp[1]
    
    # Sets status of bid to given status string
    def setBidStatus(self, status, bidID):
        db = self.get_db()
        cursor=db.cursor()

        cursor.execute("SELECT EXISTS(SELECT 1 FROM bids WHERE ID=?)", (bidID,))
        temp =  cursor.fetchone()

        cursor.execute('''
        UPDATE bids
        SET status = ?
        WHERE ID = ?
        ''',(status,bidID))
        db.commit()
        db.close()
        return 0

    # Sets status of ad to given status string
    def setAdStatus(self, status, adID):
        db = self.get_db()
        cursor=db.cursor()

        cursor.execute("SELECT EXISTS(SELECT 1 FROM ads WHERE ID=?)", (adID,))
        temp =  cursor.fetchone()

        cursor.execute('''
        UPDATE ads
        SET status = ?
        WHERE ID = ?
        ''',(status,adID))
        db.commit()
        db.close()
        return 0  
    
    # Incrememnt number of bids the user has completed
    def incrementBids(self, email):
        db = self.get_db()
        cursor=db.cursor()

        cursor.execute("SELECT * FROM accounts WHERE email=?", (ID, ))
        temp = cursor.fetchone()
        bids = temp[7]

        bids = bids + 1
        cursor.execute('''
        UPDATE accounts
        SET bidsPosted = ?
        WHERE email = ?
        ''',(bids,email))
        db.commit()
        db.close()
        return 0

    # Increment number of ads user has completed
    def incrementAds(self, email):
        db = self.get_db()
        cursor=db.cursor()

        cursor.execute("SELECT * FROM accounts WHERE email=?", (ID, ))
        temp = cursor.fetchone()
        ads = temp[6]

        ads = ads + 1
        cursor.execute('''
        UPDATE accounts
        SET adsPosted = ?
        WHERE email = ?
        ''',(ads,email))
        db.commit()
        db.close()
        return 0
    
    def getAdPrice(self, adID):
        db = self.get_db()
        cursor=db.cursor()

        cursor.execute("SELECT price FROM ads WHERE ID=?", (adID, ))
        temp = cursor.fetchone()

        self.close(db)
        return temp[0]
    

    def getAllBids(self):
        db = self.get_db()
        cursor=db.cursor()

        cursor.execute("SELECT * FROM bids", (adID, ))
        temp = cursor.fetchall()

        self.close(db)
        return temp