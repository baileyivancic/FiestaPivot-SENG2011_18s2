
from database import Database

db = Database()

ads = db.find_user_bids("test@gmail.com")
print( ads )