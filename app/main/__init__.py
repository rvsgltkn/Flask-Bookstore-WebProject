from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import UploadSet,configure_uploads,IMAGES,patch_request_class
from flask_bootstrap import Bootstrap

from .config import config_by_name


db=SQLAlchemy()
flask_bcrypt=Bcrypt()
login=LoginManager()
login.login_view='api.user_user_login'
bootstrap=Bootstrap()

photos=UploadSet('photos',IMAGES)


def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    login.init_app(app)
    bootstrap.init_app(app)
    configure_uploads(app, photos)
    patch_request_class(app)


    return app


