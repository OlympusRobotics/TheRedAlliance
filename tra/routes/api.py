import re
from tra import db
from tra.models import Admin
from flask import Blueprint, request, render_template

bp = Blueprint("api", __name__, url_prefix="/api")

MIN_USER_LEN = 6


def validate_username(username):
    """query the username and check if it is valid. Returns a message which can be directly put into the HTML"""

    msg = ""
    if len(username) > 200:
        msg = "Stop it u idiot"
    # username is taken
    elif not Admin.query.filter_by(username=username).first() is None:
        msg = "Email is taken"
    elif not re.match("[^@]+@[^@]+\.[^@]+", username):
        msg = "Email is not valid"
    return {"valid": msg}


@bp.route("/admin/is_username_valid", methods=["GET"])
def is_username_valid():
    """
    Wrapper for 'validate_username' function
    query the username and check if it is valid. Returns a message which can be directly put into the HTML
    """
    return validate_username(request.args["username"])
