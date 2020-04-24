from flask import request,render_template,make_response,url_for
from flask_restx import Resource

from app.main.model.book import Book
from ..util.dto import HomeDto
api=HomeDto.api



@api.route('/')
@api.route('/index')
class Index(Resource):

    def __init__(self,*args,**kwargs):
        self.page_size=5

    def get(self):
        page=request.args.get('page',1,type=int)
        books=Book.query.order_by(Book.created_on.desc()).paginate(page,self.page_size,False)
        next_url=url_for('api._index',page=books.next_num) if books.has_next else None
        prev_url=url_for('api._index',page=books.prev_num) if books.has_prev else None
        headers={'Content-Type':'text/html'}
        return make_response(render_template('index.html',books=books.items,next_url=next_url,prev_url=prev_url),200,headers)