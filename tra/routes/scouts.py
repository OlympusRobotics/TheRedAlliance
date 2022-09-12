from flask import redirect, request, session, render_template, flash, escape, url_for, abort, Response, Blueprint

bp = Blueprint("scouts", __name__, url_prefix="/scouts")
@bp.route("")
@bp.route("/")
@bp.route("/home")
def home():
    if "name" not in session:
        return redirect(url_for("scouts.login"))
    # if the user is not logged in, then redirect back to login
    scout = Scout.query.filter_by(name=session["name"]).first()
    if scout is None:
        return redirect(url_for("login"))
    return render_template("scout/home.html", scout=scout)

# this route handles login for scouts
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if "name" not in request.form or "code" not in request.form:
            abort(400)
        # Add the user's name to the session
        scout = Scout.query.filter_by(name=request.form["name"]).first()
        # make sure a user exists with that name
        if scout is not None:
            # check code
            if request.form["code"] == scout.code:
                # add username to session
                session["name"] = escape(request.form["name"])
                return redirect(url_for("scouts.home"))

        flash("Invalid Scout Credentials", "is-danger")
        # if the name entered is only one word, possible that user forgot to 
        # put last name
        if len(request.form["name"].split()) < 2:   
            flash("Maybe you forgot to put your last name?", category="is-warning")

    return render_template("scout/login.html")
