import secrets
from tra import db
from tra.models import Admin, Scout
from tra.helpers import authorized, sanitize
from flask import redirect, request, session, render_template, flash, escape, url_for, abort, Response, Blueprint

bp = Blueprint("admin", __name__, url_prefix="/admin")


# main admin page and panel
@bp.route("")
@bp.route("/")
def admin_page():

    admin = authorized(session)
    return render_template("admin/admin.html", admin=admin, scouts=reversed(Scout.query.all()))

# handle admin login and setup
@bp.route("/login", methods=["GET", "POST"])
def admin_login():
    
    if request.method == "POST":

        # dont allow usernames longer than 20 characters
        if len(request.form["username"]) > 20:
            flash(f"Username cannot be more than 20 characters. Your username is {len(request.form['username'])} characters long")
            return redirect(url_for("admin.admin_login"))

        # check creds
        admin = Admin.query.filter_by(username=request.form["username"])
        if request.form["username"] == admin.username \
            and request.form["password"] == admin.password:
            # set the session to the key of the admin. This is what is used to check the 
            # validity of the admin session
            admin.key = secrets.token_hex(256)
            session["admin"] = admin.key
            db.session.commit()
            return redirect(url_for("admin.admin_page"))

        flash("Invalid Admin Login Credentials", "is-danger")
        return redirect(url_for("admin.admin_login"))

    return render_template("admin/admin_login.html")

@bp.route("/register")
def register():
    return render_template("admin/admin_setup.html")

# route to create new scout
@bp.route("/scout/new", methods=["POST"])
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

@bp.route("/scout/delete/<id>", methods=["DELETE"])
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
    return Response(status=200)

@bp.route("/admin/createform")
def create_form():
    return render_template("admin/create_form.html", session=session) 

# if whoever is unauthorized, redirect them to the login page
@bp.errorhandler(403)
def unauthorized(a):
    return redirect(url_for("admin.admin_login"))

bp.register_error_handler(403, unauthorized)