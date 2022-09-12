# Common routes such as home or logging out
from flask import redirect, request, session, render_template, flash, escape, Blueprint, url_for

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    return render_template("home.html") 

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("scouts.home"))