import sqlite3
import random
def dict_factory(cursor, row):#this fixes the list.
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d
class dataDB:
	def __init__(self):
		#connecting
		self.connection = sqlite3.connect("data.db")
		self.connection.row_factory = dict_factory
		self.cursor = self.connection.cursor()
		return

	def __del__(self):
		self.connection.close()

	def getfourms(self):
		#reading
		self.cursor.execute("SELECT * FROM fourm")
		return self.cursor.fetchall()

	def createfourm(self, name, age, sentence, date, ten):
		#inserting
		self.cursor.execute("INSERT INTO fourm (name, age, sentence, date, ten) VALUES (?, ?, ?, ?, ?)", [name, age, sentence, date, ten]) 
		#this is used to run a query (? placeholder)
		self.connection.commit()
		return

	def getfourm(self, fourm_id): #this is specific fourm
		self.cursor.execute("SELECT * FROM fourm WHERE id = ?", [fourm_id])
		return self.cursor.fetchone()

	def updatefourm(self, fourm_id, name, age, sentence, date, ten):
		self.cursor.execute("UPDATE fourm SET name = ?, age = ?, sentence = ?, date = ?, ten =? WHERE id = ?", [name, age, sentence, date, ten, fourm_id])
		self.connection.commit()

	def deletefourm(self, fourm_id):
		self.cursor.execute("DELETE FROM fourm WHERE id = ?", [fourm_id])
		self.connection.commit()