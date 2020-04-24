from .. import db
from datetime import datetime

class Book(db.Model):
    __tablename__="book"
    __table_args__=(db.UniqueConstraint('name','author',name='cons_book'),)

    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    name=db.Column(db.String(50),nullable=False)
    author=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(255))
    created_on=db.Column(db.DateTime,default=datetime.utcnow())
    image_url=db.Column(db.String(250))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))








