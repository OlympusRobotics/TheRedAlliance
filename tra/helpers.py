from tra.models import Admin

def admin_set():
    return len(Admin.query.all()) != 0

