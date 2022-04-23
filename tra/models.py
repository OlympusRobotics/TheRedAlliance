from tra import db

class UserData(db.Model):#create table
	_id = db.Column("id", db.Integer, primary_key=True) # pk
	data = db.Column(db.String(1000000)) # json of scouting info per user

	def __init__(self, data):
		self.data = data