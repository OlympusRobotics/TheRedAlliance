# common routes
from . import app, db

@app.route("/test")
def test():
    return "test"