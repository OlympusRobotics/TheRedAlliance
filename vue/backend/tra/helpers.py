from flask import escape
from tra.models import Admin

def admin_set():
    return len(Admin.query.all()) != 0

def check_admin_key(admin, session):
    """check if the session key is valid"""
    if "admin" not in session:
        return False
    return admin.key == session["admin"]

def sanitize(inp : dict):
    """Escape all values in the provided dict """
    new = {}
    for arg in inp:
        new[arg] = escape(inp[arg])
    return new