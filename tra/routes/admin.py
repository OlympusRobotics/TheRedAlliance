"These routes are HTML responses ONLY"

import secrets
from tra import db
from tra.models import Admin, Form, FormQuestion, ScoutingSchedule
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
    Blueprint,
)

bp = Blueprint("admin", __name__, url_prefix="/admin")


# main admin page and panel
@bp.route("")
@bp.route("/")
def admin_page():
    admin = authorized(session)
    return render_template("admin/admin.html", admin=admin)


@bp.route("/responses/<code>")
def form_res(code):
    admin = authorized(session)
    return render_template("admin/form_res.html", admin=admin)


# handle admin login and setup
@bp.route("/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        # check creds
        admin = Admin.query.filter_by(
            username=request.form["username"]).first()
        # if an admin is found, check password
        if admin is not None:
            if (
                request.form["username"] == admin.username
                and request.form["password"] == admin.password
            ):
                # set the session to the key of the admin. This is what is used to check the
                # validity of the admin session
                set_key(admin, session)
                return redirect(url_for("admin.admin_page"))

        flash("Invalid Admin Login Credentials", "is-danger")
        return redirect(url_for("admin.admin_login"))
    if len(Admin.query.all()) == 0:
        db.session.add(Admin(username="a", password="a"))
        db.session.commit()
    return render_template("admin/admin_login.html")


@bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":

        # client already checks username. Abort if the username is not valid.
        if validate_username(request.form["username"])["valid"] != "":
            abort(400)
        admin = Admin(
            username=request.form["username"], password=request.form["password"], key=secrets.token_hex(256))

        db.session.add(admin)
        db.session.commit()
        # log the user in
        set_key(admin, session)
        flash("Account created", "is-success")
        return redirect(url_for("admin.admin_page"))

    return render_template("admin/admin_setup.html")


@bp.route("/editform", methods=["POST", "GET"])
def edit_form():
    admin = authorized(session, abort_on_fail=False)
    # if not logged in, the user probably is trying to use the form
    if admin is None:
        return redirect(url_for("main.form", code=request.args["code"]))
    # get the form and make sure it belongs to the right person
    # This is def not optimized TODO fix this
    form = Form.query.filter_by(
        code=request.args["code"], admin_id=admin.id
    ).first_or_404()
    return render_template("admin/create_form.html")

@bp.route("/makeschedule/<id>", methods=["GET"])
def create_schedule(id):
    admin = authorized(session, abort_on_fail=False)
    # if not logged in, the user probably is trying to use the form
    if admin is None:
        return redirect(url_for("main.schedule", id=id))
    
    schedule = ScoutingSchedule.query.filter_by(admin=admin, id=id).first_or_404()
    return render_template("admin/create_schedule.html")

# if whoever is unauthorized, redirect them to the login page
# this obviously only needs to be on this route
@bp.errorhandler(403)
def unauthorized(a):
    return redirect(url_for("admin.admin_login"))
