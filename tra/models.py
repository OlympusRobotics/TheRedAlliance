from tra import db

"""
Relationships:

Admin creates as many scouts as needed, scouts create ScoutResponses, 
then the Admin can view the data collected by the scouts
"""


class Admin(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)  # pk
    username = db.Column(db.String(64))
    password = db.Column(db.String(120))  # code used for accessing account

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"Admin {self.username}\nScouts: {''.join([scout.__repr__ + ' ' for scout in self.scouts])}"


class Scout(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)  # pk
    name = db.Column(db.String(64))
    code = db.Column(db.String(12))  # code used for accessing account
    responses = db.relationship("ScoutResponse", backref="scout", lazy=True)

    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __repr__(self):
        return f"< {self.name}, {self.code}, {self.id} >"


class ScoutResponse(db.Model):  # create table
    _id = db.Column("id", db.Integer, primary_key=True)  # pk
    scout_id = db.Column(db.Integer, db.ForeignKey("scout.id"))
    data = db.Column(db.String(1000000))  # json of the response provided by the scout

    def __init__(self, data):
        self.data = data
