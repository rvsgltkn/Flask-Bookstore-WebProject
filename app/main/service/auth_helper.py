from app.main.model.user import User
from .. service.blacklist_service import save_token
from flask import make_response
from flask_api import status

class Auth:

    @staticmethod
    def login_user(data):
        try:
            user=User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(password=data.get('password')):
                auth_token=User.encode_auth_token(user.id)
                if auth_token:
                    response_obj={
                        'status':'success',
                        'message':'successfully logged in',
                        'Authorization':auth_token.decode()
                    }
                    return make_response(response_obj,status.HTTP_200_OK)
                else:
                    print(e)
                    response_obj = {'status': 'fail',
                                    'message': 'try again'}

                    return make_response(response_obj, status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                response_obj={
                    'status':'fail',
                    'message':'email or password does not match'
                }
                return make_response(response_obj,status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            response_obj={'status':'fail',
                          'message':'try again'}

            return make_response(response_obj,status.HTTP_500_INTERNAL_SERVER_ERROR)


    @staticmethod
    def logout_user(data):
        if data:
            auth_token=data.split(" ")[1]
        else:
            auth_token=''

        if auth_token:
            resp=User.decode_auth_token(auth_token)
            if not isinstance(resp,str):
                return save_token(token=auth_token)
            else:
                response_obj={
                    'status':'fail',
                    'message':resp
                }
                return make_response(response_obj,status.HTTP_401_UNAUTHORIZED)
        else:
            response_obj={
                'status':'fail',
                'message':'provide a valid token'
            }
            return make_response(response_obj,status.HTTP_403_FORBIDDEN)


    @staticmethod
    def get_logged_in_user(new_request):
        auth_token=new_request.headers.get('Authorization')
        if auth_token:
            resp=User.decode_auth_token(auth_token)
            if not isinstance(resp,str):
                user=User.query.filter_by(id=resp).first()
                response_obj={
                    'status':'success',
                    'data':{
                        'user_id':user.id,
                        'email':user.email,
                        'admin':user.admin,
                        'registered_on':str(user.registered_on)
                    }
                }

                return make_response(response_obj,status.HTTP_200_OK)
            else:
                response_obj={
                    'status':'fail',
                    'message':resp
                }
                return make_response(response_obj,status.HTTP_401_UNAUTHORIZED)

        else:
            response_obj={
                'status':'fail',
                'message':'Please provide a valid token'
            }
            return make_response(response_obj,status.HTTP_401_UNAUTHORIZED)