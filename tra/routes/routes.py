# Common routes such as home or logging out
from ..models import Form
from flask import (
    redirect,
    request,
    session,
    render_template,
    flash,
    escape,
    Blueprint,
    url_for,
)

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    return redirect(url_for("admin.admin_login"))

@bp.route("/<code>")
def form(code):
    if Form.query.filter_by(code=code).first() is None:
        return redirect(url_for("admin.admin_page"))
    return render_template("public/form.html")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin.admin_login"))
