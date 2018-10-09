
from database import Database

db = Database()

ads = db.find_user_ads("test@gmail.com")
bids = db.find_user_bids("test@gmail.com")
print(ads)
print(bids)