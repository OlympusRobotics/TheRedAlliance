from tra import db
import datetime, string, random

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
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(
        db.String(120), nullable=False
    )  # code used for accessing account
    key = db.Column(db.String(512), nullable=True)  # key for authenticating the admin
    forms = db.relationship("Form", backref="admin")

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"Admin {self.username} | {self.password} | {self.code}"


class Form(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)  # pk
    code = db.Column(db.String(6), unique=True, nullable=False)  # the url of the form
    name = db.Column(db.String(64), unique=True, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"), nullable=False)
    questions = db.relationship("FormQuestion", backref="form", lazy=True)

    def __init__(self, name, questions):
        self.name = name
        self.code = "".join(
            [random.choice(string.ascii_letters) for _ in range(6)]
        ).upper()  # create 5 digit code
        # create FormQuestion model for each question in the form
        self.questions = questions


class FormQuestion(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)  # pk
    prompt = db.Column(db.String(200), nullable=True)
    question_format = db.Column(db.Text, nullable=False)
    responses = db.relationship("QuestionResponse", backref="question", lazy=True)
    form_id = db.Column(db.Integer, db.ForeignKey("form.id"), nullable=False)

    def __init__(self, prompt, question_format):
        self.prompt = prompt
        self.question_format = question_format


class QuestionResponse(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)  # pk
    response = db.Column(db.Text, nullable=True)
    question_id = db.Column(
        db.Integer, db.ForeignKey("form_question.id"), nullable=False
    )

    def __init__(self, response):
        self.response = response
