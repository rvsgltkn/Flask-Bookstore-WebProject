from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.book_controller import api as book_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.main_controller import api as main_ns

blueprint=Blueprint('api',__name__)

api=Api(blueprint,
        title='FLASK BOOK STORE',
        version='1.0',
        description='simple bookstore app'
        )

api.add_namespace(main_ns,path='')
api.add_namespace(user_ns,path='/user')
api.add_namespace(book_ns,path='/book')
api.add_namespace(auth_ns,path='/auth')


