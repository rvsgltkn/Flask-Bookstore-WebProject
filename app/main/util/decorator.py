from functools import wraps
from flask import request,make_response
from flask_api import status

from app.main.service.auth_helper import Auth



def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        resp=Auth.get_logged_in_user(request)
        data=resp.json
        token=data.get('data')
        if not token:
            return resp

        return f(*args,**kwargs)
    return decorated

