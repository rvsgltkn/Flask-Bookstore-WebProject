from flask_restx import Namespace,fields

class AuthDto:
    api=Namespace('auth',description='authenticaton related operations')
    user_auth=api.model('auth_details',{
        'email':fields.String(required=True,description='The email address'),
        'password':fields.String(required=True,description='The user password')
    })

class UserDto:
    api=Namespace('user',description='user related operations')
    user=api.model('user',{
        'email':fields.String(required=True,description='user email address'),
        'username':fields.String(required=True,description='user username'),
        'password':fields.String(required=True,description='user password'),
        'public_id':fields.String(description='user identifier')
    })

class BookDto:
    api=Namespace('book',description='book related operations')
    book=api.model('book',{
        'name':fields.String(required=True,description='book name'),
        'author':fields.String(required=True,description='book author name'),
        'description':fields.String(description='book description')
    })


class HomeDto:
    api=Namespace('',description='main operations')