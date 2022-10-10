# This file allows for the package to be ran directly
# instead of having to be installed every time
from tra import app, db
from .models import Admin

def setup():
    db.drop_all()
    db.create_all()
    app.debug = True
    # create test account
    admin = Admin("a", "a")
    db.session.add(admin)
    db.session.commit()
    app.run(host="127.0.0.1", port=5000)

setup()