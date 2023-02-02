import secrets
from flask import escape, abort
from tra.models import Admin


def authorized(session, abort_on_fail=True) -> Admin:
    """
    Finds the admin corresponding to the given session key.
    If there is no admin matching the key, it returns None.
    @param {abort_on_fail} boolean - will not abort 403 and instead returns None on failed auth
    """
    if "admin" not in session:
        if not abort_on_fail:
            return None
        abort(403)
    admin = Admin.query.filter_by(key=session["admin"]).first()
    if admin is None and abort_on_fail:
        print("aborting here")
        abort(403)
    return admin

def set_key(admin, session) -> None:
    session["admin"] = admin.key


def sanitize(inp: dict):
    """Escape all values in the provided dict"""
    new = {}
    for arg in inp:
        new[arg] = escape(inp[arg])
    return new
