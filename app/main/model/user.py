from .. import db,flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from .. config import key
from flask_login import UserMixin
from app.main import login

class User(UserMixin,db.Model):
    __tablename__="user"

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.String(255),unique=True,nullable=False)
    registered_on=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow)
    admin=db.Column(db.Boolean,nullable=False,default=False)
    public_id=db.Column(db.String(100),unique=True)
    username=db.Column(db.String(50),unique=True)
    password_hash=db.Column(db.String(100))
    books=db.relationship('Book',backref='user',lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password : write field only')


    @password.setter
    def password(self,password):
        self.password_hash=flask_bcrypt.generate_password_hash(password).decode('utf-8')


    def check_password(self,password):
        return flask_bcrypt.check_password_hash(self.password_hash,password)

    def __repr__(self):
        return "<User '{}' >".format(self.username)

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates auth token
        :param self:
        :param user_id:
        :return: string
        """

        try:
            payload={
                'exp':datetime.datetime.utcnow()+datetime.timedelta(days=1,seconds=5),
                'iat':datetime.datetime.utcnow(),
                'sub':user_id
            }
            return jwt.encode(payload,key,'HS256')
        except Exception as e:
            return e


    @staticmethod
    def decode_auth_token(auth_token):
        """

        :param auth_token:
        :return:integer|string
        """

        try:
            payload=jwt.decode(auth_token,key)
            is_blacklisted_token=BlacklistToken.check_authtoken(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again'
        except jwt.InvalidSignatureError:
            return 'Invalid Token. Please log in again'

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))