from flask import request,make_response,render_template,redirect,url_for,flash
from flask_restx import Resource
from flask_login import current_user,login_user,logout_user,login_required
from werkzeug.urls import url_parse

from .. util.dto import UserDto
from .. service.user_service import save_new_user,get_all_users,get_user
from ..forms.user_forms import LoginForm,RegistrationForm,ProfileEditForm
from  app.main.model.user import User as modelUser
from app.main import db

api=UserDto.api
_user=UserDto.user

#service routes**************************
@api.route('/')
class UserList(Resource):

    @api.doc('list of registered users')
    @api.marshal_list_with(_user,envelope='data')
    def get(self):
        return get_all_users()


    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        data=request.json
        return save_new_user(data)


@api.route('/<public_id>')
@api.param('public_id','The User Identifier')
@api.response(404,'User not found')
class User(Resource):

    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self,public_id):
        user= get_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user

#web routes******************************
@api.route('/login')
class UserLogin(Resource):

    def __init__(self,*args,**kwargs):
        self.form = LoginForm()
        self.headers = {'Content-Type': 'text/html'}

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('api._index'))
        return make_response(render_template('login.html',title='Sign In', form=self.form), 200, self.headers)

    def post(self):
        if self.form.validate_on_submit():
            user = modelUser.query.filter_by(email=self.form.email.data).first()
            if user is None or not user.check_password(self.form.password.data):
                flash('invalid username or password')
                return redirect(url_for('api.user_user_login'))

            login_user(user,remember=self.form.remember_me.data)
            next_page=request.args.get('next')
            if not next_page or url_parse(next_page).netloc!='':
                next_page=url_for('api._index')
            return redirect(next_page)
        return make_response(render_template('login.html', title='Sign In', form=self.form), 200, self.headers)


@api.route('/logout')
class UserLogout(Resource):

    def get(self):
        logout_user()
        return redirect(url_for('api._index'))

@api.route('/register')
class UserRegister(Resource):

    def __init__(self,*args,**kwargs):
        self.form=RegistrationForm()
        self.headers={'Content-Type': 'text/html'}

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('api._index'))
        return make_response(render_template('register.html', title='Register', form=self.form), 200, self.headers)

    def post(self):
        if self.form.validate_on_submit():
            user=modelUser(email=self.form.email.data,username=self.form.username.data,password=self.form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('User registered successufly')
            return redirect(url_for('api.user_user_login'))
        return make_response(render_template('register.html', title='Register', form=self.form), 200, self.headers)


@api.route('/edit_profile')
class UserProfile(Resource):

    def __init__(self,*args,**kwargs):
        self.form=ProfileEditForm()
        self.headers = {'Content-Type': 'text/html'}
        self.user = modelUser.query.filter_by(id=current_user.id).first()

    @login_required
    def get(self):
        return make_response(render_template('profile.html',title='Profile',form=self.form, user=self.user),200,self.headers)

    def post(self):
        if self.form.validate_on_submit():

            self.user.username=self.form.username.data
            self.user.password=self.form.password.data
            db.session.add(self.user)
            db.session.commit()
            flash('User updated successfully')
            return redirect(url_for('api._index'))

        return make_response(render_template('profile.html', title='Profile', form=self.form, user=self.user), 200, self.headers)
