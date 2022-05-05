import secrets
from tra import db, app
from tra.models import ScoutResponse, Scout, Admin
from tra.helpers import admin_set, check_admin_key, sanitize
from flask import redirect, request, session, render_template, flash, escape, url_for, abort, Response


@app.route("/")
@app.route("/home")
def home():
    if "admin" in session:
        redirect(url_for('admin_page'))

    if "name" not in session:
        return redirect(url_for("login"))
    # if the user is not logged in, then redirect back to login
    scout = Scout.query.filter_by(name=session["name"]).first()
    if scout is None:
        return redirect(url_for("login"))
    return render_template("home.html", scout=scout)

# this route handles login for scouts
@app.route("/login", methods=["GET", "POST"])
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
                return redirect(url_for("home"))

        flash("Invalid Scout Credentials", "is-danger")
        # if the name entered is only one word, possible that user forgot to 
        # put last name
        if len(request.form["name"].split()) < 2:   
            flash("Maybe you forgot to put your last name?", category="is-warning")

    return render_template("login.html")

# handle admin login and setup
@app.route("/login/admin", methods=["GET", "POST"])
def admin_login():
    
    if request.method == "POST":
        if "username" not in request.form or "password" not in request.form:
            abort(400)

        # dont allow usernames longer than 20 characters
        if len(request.form["username"]) > 20:
            flash(f"Username cannot be more than 20 characters. Your username is {len(request.form['username'])} characters long")
            return redirect(url_for("admin_login"))

        # admin account still needs to be set
        if not admin_set():
            new_admin = Admin(escape(request.form["username"]), request.form["password"])
            db.session.add(new_admin)
            db.session.commit()
            flash(f"Admin account {new_admin.username} created", "is-info")
            return redirect(url_for("admin_login"))

        # admin account has already been created. check creds
        admin = Admin.query.all()[0]
        if request.form["username"] == admin.username \
            and request.form["password"] == admin.password:
            # set the session to the key of the admin. This is what is used to check the 
            # validity of the admin session
            admin.key = secrets.token_hex(256)
            session["admin"] = admin.key
            db.session.commit()
            return redirect(url_for("admin_page"))

        flash("Invalid Admin Login Credentials", "is-danger")
        return redirect(url_for("admin_login"))

    # if no admin exists, then show the admin setup page
    if not admin_set():
        flash("Looks like a scouting admin needs to be setup. Please set up an account here to begin managing scouts", category="is-primary")
        return render_template("admin_setup.html")

    # otherwise show normal login page
    return render_template("admin_login.html")

# main admin page and panel
@app.route("/admin")
def admin_page():
    # admin hasnt been set yet
    if not admin_set():
        return redirect(url_for("admin_login"))
    
    admin = Admin.query.all()[0]
    if not check_admin_key(admin, session):
            abort(403)
    return render_template("admin.html", admin=admin, scouts=reversed(Scout.query.all()))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# route to create new scout
@app.route("/admin/scout/new", methods=["POST"])
def new_scout():
    admin = Admin.query.all()[0]
    # admin required
    if not check_admin_key(admin, session):
        abort(403)
    if "name" not in request.form or "code" not in request.form:
        abort(400)
    
    form = sanitize(request.form)
    scout_names = [scout.name for scout in Scout.query.all()]
    if form["name"] in scout_names:
        flash(f"{form['name']} is already a scout", "is-danger")
        return Response(status=409)

    scout = Scout(form["name"], form["code"])
    db.session.add(scout)
    db.session.commit()
    flash(f"{scout.name} added successfully", "is-success")
    return Response(status=200)

@app.route("/admin/scout/delete/<id>", methods=["DELETE"])
def delete_scout(id):
    admin = Admin.query.all()[0]
    if not check_admin_key(admin, session):
        abort(403)
    # this is the query object which can be deleted wiht db.session.delete()
    scout = Scout.query.filter_by(id=int(id))
    if scout is None:
        abort(404)
                # get the scout obejct from the query
    flash(f"{scout.first().name} has been deleted", "is-primary")
    scout.delete()
    db.session.commit()
    return Response(status=200form.namegtform.namegtgg)

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
