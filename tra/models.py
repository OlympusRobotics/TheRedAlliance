from tra import db
	
class Scout(db.Model):
	id = db.Column("id", db.Integer, primary_key=True) # pk
	name = db.Column(db.String(64))
	code = db.Column(db.String(12)) # code used for accessing account
	responses = db.relationship('ScoutResponse', backref='scout', lazy=True)
	def __init__(self, name, code):
		self.name = name
		self.code = code
	
	def __repr__(self):
		return f"< {self.name}, {self.code}, {self.id} >"

class ScoutResponse(db.Model):#create table
	_id = db.Column("id", db.Integer, primary_key=True) # pk
	scout_id = db.Column(db.Integer, db.ForeignKey('scout.id'))
	data = db.Column(db.String(1000000)) # json of the response provided by the scout
	def __init__(self, data):
		self.data = data
