from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import HTTPException


app = Flask(__name__)  # instance of flask
app.config['UPLOAD_FOLDER'] = "tra/static/pictures"
app.secret_key = b"\x14J\xff\x00\x9c\xf3\x80\xab\xda\r8\xa9\xad3D\xab"  # encryption key for session data. Obviously this will change in production
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///data.sqlite3"  # config for database. data.sqlite3 is the table name
app.config["SQLALCEHMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=3)
db = SQLAlchemy(app)  # create a database object

limiter = Limiter(get_remote_address, app=app, storage_uri="memory://")

# Register all the blueprints
from .routes.admin import bp as admin_routes
from .routes.routes import bp as main_routes
from .routes.api import bp as api_routes

app.register_blueprint(admin_routes)
app.register_blueprint(main_routes)
app.register_blueprint(api_routes)
app.app_context().push()


def main():
    db.create_all()
    app.debug = True
    app.run(host="127.0.0.1", port=5000)
