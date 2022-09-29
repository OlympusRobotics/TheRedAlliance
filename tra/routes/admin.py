import secrets
from tra import db
from tra.models import Admin
from .api import validate_username
from tra.helpers import authorized, sanitize, set_key
from flask import (
    redirect,
    request,
    session,
    render_template,
    flash,
    escape,
    url_for,
    abort,
    Response,
    Blueprint,
)

bp = Blueprint("admin", __name__, url_prefix="/admin")


# main admin page and panel
@bp.route("")
@bp.route("/")
def admin_page():

    admin = authorized(session)
    return render_template("admin/admin.html", admin=admin)


# handle admin login and setup
@bp.route("/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        # check creds
        admin = Admin.query.filter_by(username=request.form["username"]).first()
        # if an admin is found, check password
        if admin is not None:
            if (
                request.form["username"] == admin.username
                and request.form["password"] == admin.password
            ):
                # set the session to the key of the admin. This is what is used to check the
                # validity of the admin session
                set_key(admin, session, db)
                return redirect(url_for("admin.admin_page"))

        flash("Invalid Admin Login Credentials", "is-danger")
        return redirect(url_for("admin.admin_login"))
    return render_template("admin/admin_login.html")


@bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":

        # client already checks username. Abort if the username is not valid.
        if validate_username(request.form["username"])["valid"] != "":
            abort(400)
        admin = Admin(request.form["username"], request.form["password"])
        db.session.add(admin)
        db.session.commit()
        # log the user in
        set_key(admin, session, db)
        flash("Account created", "is-success")
        return redirect(url_for("admin.admin_page"))

    return render_template("admin/admin_setup.html")


@bp.route("/admin/createform")
def create_form():
    admin = authorized(session)
    return render_template("admin/create_form.html", admin=admin)


# if whoever is unauthorized, redirect them to the login page
@bp.errorhandler(403)
def unauthorized(a):
    return redirect(url_for("admin.admin_login"))


bp.register_error_handler(403, unauthorized)
