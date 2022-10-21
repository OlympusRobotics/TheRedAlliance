from tra import db
import datetime, string, random, json

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

    def __repr__(self):
        return f"Admin {self.username} | {self.password} | {self.code}"


class Form(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)  # pk
    code = db.Column(db.String(6), unique=True, nullable=False)  # the url of the form
    name = db.Column(db.String(64), default="FRC Scouting Form")
    draft = db.Column(db.Boolean(), default=True)
    json_repr = db.Column(
        db.Text, nullable=False, default=json.dumps({})
    )  # the full json representation of the form
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"), nullable=False)
    questions = db.relationship("FormQuestion", backref="form", lazy=True)


class FormQuestion(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)  # pk
    code = db.Column(
        db.String(6), unique=True, nullable=False
    )  # the identifier that will be used in the JS
    form_id = db.Column(db.Integer, db.ForeignKey("form.id"), nullable=False)
    data = db.Column(db.Text, nullable=False)  # json object that contains format
    responses = db.Column(db.Text, nullable=True)  # json list of objects

    def __repr__(self):
        return f"{self.code} | {self.data} |{self.responses} "
