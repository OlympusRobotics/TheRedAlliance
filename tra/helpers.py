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
