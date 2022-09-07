from .. import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(128), nullable=False) # secret uuid. Used for auth
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} | {self.email} | {self.uuid} | {self.hash}"

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form = db.Column(db.Text, nullable=False) 
    user = db.relationship('User', backref=db.backref('forms', lazy=True))


