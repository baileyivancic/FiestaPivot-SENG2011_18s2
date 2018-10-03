
from database import Database

db = Database()

ads = db.fetch_ads()
print( ads[0][0] )