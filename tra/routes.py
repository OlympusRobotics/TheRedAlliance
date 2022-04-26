from re import L
from tra import db, app
from tra.models import ScoutResponse, Scout
from flask import redirect, request, session, render_template, flash, escape, url_for


@app.route("/")
@app.route("/home")
def home():
    if "name" not in session:
        return redirect(url_for("login"), admin=None)
    # if the session name exists but has nothing in it, redirect to login page
    scout = Scout.query.filter_by(name=session["name"]).first()
    if scout is None:
        return redirect(url_for("login"))
    return render_template("home.html", scout=scout)

# this route handles login for scouts
@app.route("/login", methods=["GET", "POST"])
def login(admin=None):
    if request.method == "POST":
        if "name" in request.form and "code" in request.form:
            # Add the user's name to the session
            scout = Scout.query.filter_by(name=request.form["name"]).first()
            # make sure a user exists with that name
            if scout is not None:
                # check code
                if request.form["code"] == scout.code:
                    # add username to session
                    session["name"] = escape(request.form["name"])
                    return redirect(url_for("home"))

            flash("Invalid Scout Credentials", "is-danger")
            if len(request.form["name"].split()) < 2:   
                flash("Maybe you forgot to put your last name?", category="is-warning")

    return render_template("login.html")

@app.route("/login/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if "username" in request.form and "password" in request.form:
            pass

    return render_template("admin_setup.html")


# This route is for testing writing to sql database
@app.route("/test", methods=["POST", "GET"])  # specify methods and route
def test():
    if request.method == "POST":
        session.permanent = True  # set permanent session
        form_data = request.form["scout_data"]

        # found_user = users.query.filter_by(name=user).first() #what_to_access.perform_a_query.find_all_that_meet_criteria.grab_first_result    This is how to find a user
        usr_data = ScoutResponse(form_data)
        db.session.add(usr_data)
        db.session.commit()
        for i in UserData.query.all():
            print(i.data)

        flash("Data recieved!", "info")

    return render_template("scouting.html")
