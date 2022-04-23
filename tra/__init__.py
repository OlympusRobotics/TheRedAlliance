from flask import Flask

app = Flask(__name__)
# this just has to be here for magic reasons
from tra import routes

def main():
    app.run("0.0.0.0", 8000, debug=True)