import uuid
from datetime import datetime

from app.main import db
from app.main.model.user import User
from flask import make_response
from flask_api import status

def save_new_user(data):
    user=User.query.filter_by(email=data.get('email')).first()
    if not user:
        new_user=User(public_id=str(uuid.uuid4()),
                      email=data.get('email'),
                      username=data.get('username'),
                      password=data.get('password'),
                      registered_on=datetime.utcnow()
                      )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_obj={'status':'fail',
                      'message':'User already exist'}

        return make_response(response_obj,status.HTTP_409_CONFLICT)


def get_all_users():
    return User.query.all()

def get_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()

def generate_token(user):
    try:
        auth_token=user.encode_auth_token(user.id)
        response_obj={
            'status':'success',
            'message':'succesfully registered',
            'Authorization':auth_token.decode()
        }
        return make_response(response_obj,status.HTTP_201_CREATED)
    except Exception as e:
        response_obj={
            'status':'fail',
            'message':'some error occured. please try again'
        }

        return make_response(response_obj,status.HTTP_401_UNAUTHORIZED)