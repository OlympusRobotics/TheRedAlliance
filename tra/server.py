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
