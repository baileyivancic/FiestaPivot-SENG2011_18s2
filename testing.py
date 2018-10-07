
from database import Database

db = Database()

ads = db.find_bid("test@gmail.com")
print( ads )