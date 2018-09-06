import os
import sqlite3

class Database(object):
	def __init__(self):
		pass

	def first_run(self):
		db = sqlite3.connect('database.db')
		cursor = db.cursor()

		#create table for authenticated users
		cursor.execute('''CREATE TABLE IF NOT EXISTS
                		  	loginDetails(userID 		INT  PRIMARY KEY  NOT NULL,
					  					 username 		TEXT,
							 		 	 password		TEXT)''')

		#create table for saved recipes
		#recipeIngredients - comma separated string of recipeIngredients?
		#cursor.execute('''CREATE TABLE IF NOT EXISTS
		 #			  	  	savedRecipes(recipeID			INT		PRIMARY KEY NOT NULL,
		#								 userID				INT 	FOREIGN KEY NOT NULL,
		#								 recipename			TEXT,
		#								 recipeIngredients	TEXT )''')


		#cursor.execute('''CREATE TABLE IF NOT EXISTS
		 #			  	  	savedIngredients(ingredientID	INT		PRIMARY KEY NOT NULL,
		#									 userID 		INT 	FOREIGN KEY NOT NULL,
		#								 	 ingredient		TEXT )''')

		#create table for saved recipes
		cursor.execute('''CREATE TABLE IF NOT EXISTS
					  	  	savedPlans(planID		INT		PRIMARY KEY NOT NULL,
									   userID		INT 	NOT NULL,
									   recipes		TEXT,
									   FOREIGN KEY (userID) REFERENCES loginDetails (userID))''')

		db.commit()
		db.close()


	def savePlan(self, userID, recipes):
		print(userID)
		print("Hey, we went into this function")
		db = sqlite3.connect('database.db')
		cursor = db.cursor()
		cursor.execute('''SELECT MAX(planID) FROM savedPlans''')
		i = cursor.fetchone()
		if i[0]!=None:
			x = i[0] + 1
		else:
			x = 1
		cursor.execute('''INSERT INTO savedPlans (planID,userID,recipe) VALUES (?,?,?)''',(planID,userID,recipes))
		db.commit()
		db.close()
db.close()