from flask import escape, abort
from tra.models import Admin


def authorized(session) -> Admin:
    """
    Finds the admin corresponding to the given session key.
    If there is no admin matching the key, it returns None.
    """
    if "admin" not in session:
        abort(403)
    admin = Admin.query.filter_by(key=session["admin"]).first()
    if admin is None:
        abort(403)
    return admin

def sanitize(inp : dict):
    """Escape all values in the provided dict """
    new = {}
    for arg in inp:
        new[arg] = escape(inp[arg])
    return new