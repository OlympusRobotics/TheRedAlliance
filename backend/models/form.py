from .. import db

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form = db.Column(db.Text, nullable=False) 
    user = db.relationship('User', backref=db.backref('forms', lazy=True))


