import secrets
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


def set_key(admin, session, db) -> None:
    """Creates a new key for the admin, commits it to db, and adds to session"""
    admin.key = secrets.token_hex(256)
    db.session.commit()
    session["admin"] = admin.key


def sanitize(inp: dict):
    """Escape all values in the provided dict"""
    new = {}
    for arg in inp:
        new[arg] = escape(inp[arg])
    return new
