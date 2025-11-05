from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def check_auth(*args, **kwargs):
        if not session.get('id'):
            return redirect(url_for('authentification_controller.authentification'))
        return f(*args, **kwargs)
    return check_auth