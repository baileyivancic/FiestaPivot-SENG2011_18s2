
from database import Database

db = Database()

ads = db.find_user_ads("test@gmail.com")
print( ads )