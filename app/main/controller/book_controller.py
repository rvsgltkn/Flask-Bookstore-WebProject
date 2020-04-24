from flask import request,render_template,make_response,url_for,flash,redirect
from flask_restx import Resource
from flask_login import current_user,login_required
from flask_api import status

from .. util.dto import BookDto
from .. service.book_service import save_book,get_all_book,get_book_byid
from ..util.decorator import token_required

from ..forms.book_forms import BookForm,BookEditForm
from app.main import db,photos
from app.main.model.book import Book as modelBook
from app.main.model.user import User

api=BookDto.api
_book=BookDto.book

@api.route('/')
class BookList(Resource):

    @api.doc('get all books')
    @api.marshal_list_with(_book,envelope='data')
    def get(self):
        return get_all_book()

    @token_required
    @api.doc('save new book')
    @api.expect(_book)
    def post(self):
        auth_token = request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                data=request.json
                return save_book(data,user)

            else:
                response_obj = {
                'status': 'fail',
                'message': resp
                }
                return make_response(response_obj, status.HTTP_401_UNAUTHORIZED)
        else:
            response_obj = {
                'status': 'fail',
                'message': 'Please provide a valid token'
            }
            return make_response(response_obj, status.HTTP_401_UNAUTHORIZED)

@api.route('/<id>')
@api.param('id','The Book Identifier')
@api.response(401,'Book not found')
class Book(Resource):

    @api.doc('get a book')
    @api.marshal_with(_book)
    def get(self,id):
        book=get_book_byid(id)
        if not book:
            api.abort(404)

        return book


####web routes*****************8

@api.route('/book')
class BookAdd(Resource):

    def __init__(self,*args,**kwargs):
        self.form=BookForm()
        self.headers = {'Content-Type': 'text/html'}

    @login_required
    def get(self):
        return make_response(render_template('book.html',form=self.form, title='Book'),200,self.headers)


    def post(self):
        print('disardayim')
        if self.form.validate_on_submit():
            print('icerdeyim')
            try:
                filename=photos.save(self.form.photo.data)
                file_url=photos.url(filename)
            except Exception as e:
                print('Error :',e)

            new_book=modelBook(
                name=self.form.name.data,
                author=self.form.author.data,
                description=self.form.description.data,
                user=current_user,
                image_url=file_url
            )
            db.session.add(new_book)
            db.session.commit()
            print('book created successfully')
            flash('Book created successfully')

        return make_response(render_template('book.html', form=self.form, title='Book Edit'), 200, self.headers)


@api.route('/book/<book_id>')
class BookEdit(Resource):

    def __init__(self,*args,**kwargs):
        self.form=BookEditForm()
        self.headers = {'Content-Type': 'text/html'}

    @login_required
    def get(self,book_id):
        book=modelBook.query.filter_by(id=book_id).first_or_404()
        self.form.description.data =book.description
        return make_response(render_template('book_edit.html',form=self.form, title='Book Edit',book=book),200,self.headers)


    def post(self,book_id):
        book = modelBook.query.filter_by(id=book_id).first_or_404()
        if self.form.validate_on_submit():
            book.name=self.form.name.data
            book.author=self.form.author.data
            book.description=self.form.description.data
            db.session.add(book)
            db.session.commit()
            print('Book updated successfully')
            flash('Book updated successfully')


        return make_response(render_template('book_edit.html', form=self.form, title='Book Edit', book=book), 200, self.headers)

@api.route('/book/delete/<book_id>')
class BookDelete(Resource):

    def __init__(self,*args,**kwargs):
        self.form=BookEditForm()
        self.headers = {'Content-Type': 'text/html'}

    @login_required
    def get(self,book_id):
        book=modelBook.query.filter_by(id=book_id).first_or_404()
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('api._index'))