import datetime
import secrets
from tra import db

"""
Relationships:

Admin creates as many scouts as needed, scouts create ScoutResponses, 
then the Admin can view the data collected by the scouts.

Custom forms are created and each question is stored as its own table 
using the FormQuestion model.
Scouts then sumbit ScoutResponses to them.
"""


class Admin(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)  # pk
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(120))  # code used for accessing account
    key = db.Column(db.String(512)) # key for authenticating the admin

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"Admin {self.username}"


class Scout(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)  # pk
    name = db.Column(db.String(64), unique=True)
    code = db.Column(db.String(12))  # code used for accessing account

    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __repr__(self):
        return f"< {self.name}, {self.code}, {self.id} >"

class Form(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)  # pk
    name = db.Column(db.String(64), unique=True)
    questions = db.relationship("FormQuestion", backref="form", lazy=True)
    responses = db.relationship("ScoutResponse", backref="form", lazy=True)

    def __init__(self, name, questions):
        self.name = name
        # create FormQuestion model for each question in the form
        self.questions = map(FormQuestion, questions)

# This is what is actually rendered into HTML
class FormQuestion(db.Model):
    form_id = db.Column(db.Integer, db.ForeignKey("form.id"), primary_key=True)
    question_type = db.Column(db.Text) # the type of question e.i. radio button, check boxes, text input, etc
    question_prompt = db.Column(db.String(200)) # the prompt for the question that will be shown 
    stats = db.Column(db.Text) # this stores stats such as how many people answered a certain way

    def __init__(self, question):
        self.question_prompt = question["prompt"]
        self.question_type = question["type"]

class ScoutResponse(db.Model):  # create table
    form_id = db.Column(db.Integer, db.ForeignKey("form.id"), primary_key=True)
    data = db.Column(db.String(1000000))  # json of the response provided by the scout
    date = db.Column(db.DateTime)

    def __init__(self, data):
        self.data = data
        self.date = datetime.datetime.now()
        self.form = form 
