from app.main import db
from app.main.model.blacklist import BlacklistToken
from flask_api import status
from flask import make_response

def save_token(token):
    blacklist_token=BlacklistToken(token)

    try:
        db.session.add(blacklist_token)
        db.session.commit()

        response_obj={
            'status':'success',
            'message':'Successfuly logged out'
        }

        return make_response(response_obj,status.HTTP_200_OK)

    except Exception as e:
        response_obj={'status':'fail',
                      'message':e}

        return make_response(response_obj,status.HTTP_200_OK)

