
from database import Database

db = Database()

ads = db.find_user_ads("another@gmail.com")
bids = db.find_user_bids("another@gmail.com")
print(ads)
print(bids)