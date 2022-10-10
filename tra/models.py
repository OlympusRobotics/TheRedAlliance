from tra import db
import datetime, string, random

"""
Relationships:

Admins have accounts which contain Forms. 
Forms are composed of FormQuestions which store their own response data.
"""


class Admin(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)  # pk
    username = db.Column(
        db.String(64), unique=True, nullable=False
    )  # actually is email lol
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
    draft = db.Column(db.Boolean(), default=True)
    json_repr = db.Column(
        db.Text, nullable=False
    )  # the full json representation of the form
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"), nullable=False)
    questions = db.relationship("FormQuestion", backref="form", lazy=True)

    def __init__(self, code, name, json_repr):
        self.name = name
        self.code = code
        # create FormQuestion model for each question in the form
        self.json_repr = json_repr


class FormQuestion(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)  # pk
    form_id = db.Column(db.Integer, db.ForeignKey("form.id"), nullable=False)
    data = db.Column(db.Text, nullable=False)  # json object that contains format
    responses = db.Column(db.Text, nullable=True)  # json list of objects

    def __init__(self, question_format):
        self.data = question_format
