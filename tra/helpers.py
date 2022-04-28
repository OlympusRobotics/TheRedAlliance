from tra.models import Admin

def admin_set():
    return len(Admin.query.all()) != 0

def check_admin_key(admin, session):
    """check if the session key is valid"""
    if "admin" not in session:
        return False
    return admin.key == session["admin"]