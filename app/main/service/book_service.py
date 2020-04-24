from app.main.model.book import Book
from app.main import db
from flask import make_response
from flask_api import status

def save_book(data,user):
    book=Book.query.filter_by(name=data.get('name'),author=data.get('author')).first()
    if not book:
        new_book=Book(name=data.get('name'),author=data.get('author'),description=data.get('description'),user=user)
        save_data(new_book)
        response_obj={'status':'success',
                      'message':'Successfuly saved'}

        return make_response(response_obj,status.HTTP_201_CREATED)
    else:
        response_obj={'status':'fail',
                      'message':'Book is already exist'}
        return make_response(response_obj,status.HTTP_409_CONFLICT)



def get_all_book():
    return Book.query.all()

def get_book_byid(id):
    return Book.query.filter_by(id=id).first()

def save_data(data):
    db.session.add(data)
    db.session.commit()

