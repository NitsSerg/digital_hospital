from flask import abort
from flask_login import current_user

def role_required(allowed_roles):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return abort(401)  
            if current_user.role not in allowed_roles:
                return abort(403)  
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__ 
        return wrapper
    return decorator

