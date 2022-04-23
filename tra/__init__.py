from flask import Flask

app = Flask(__name__)
app.secret_key = '9174d8959d3b00b2ca44f6e0114621f3b1fe138c1de17da6509a76838171653a'
# this just has to be here for magic reasons
from tra import routes


def main():
    app.run("0.0.0.0", 8000, debug=True)
