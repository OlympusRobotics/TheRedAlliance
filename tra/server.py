
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) #instance of flask
app.secret_key = b'\x14J\xff\x00\x9c\xf3\x80\xab\xda\r8\xa9\xad3D\xab'  #encryption key for session data
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite3" #config for database. data.sqlite3 is the table name
app.config["SQLALCEHMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app) #create a database object

class UserData(db.Model):#create table
	_id = db.Column("id", db.Integer, primary_key=True) # pk
	data = db.Column(db.String(1000000)) # json of scouting info per user

	def __init__(self, data):
		self.data = data

@app.route("/", methods=["POST", "GET"])  # specify methods and route
def login():
	if request.method == "POST":
		session.permanent = True # set permanent session
		form_data = request.form["scout_data"]

		#found_user = users.query.filter_by(name=user).first() #what_to_access.perform_a_query.find_all_that_meet_criteria.grab_first_result    This is how to find a user
		usr_data = UserData(form_data)
		db.session.add(usr_data)
		db.session.commit()
		for i in UserData.query.all():
			print(i.data)

		flash("Data recieved!", "info")
	
	return render_template("scouting.html")

if __name__ == "__main__":
	db.create_all()
	app.debug = True
	app.run(host="127.0.0.1", port = 5000)

