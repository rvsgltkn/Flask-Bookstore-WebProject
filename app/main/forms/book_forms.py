from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired,FileAllowed,FileField
from app.main import photos

class BookForm(FlaskForm):
    photo=FileField('Book Image',validators=[FileAllowed(photos,u'Image only'),FileRequired(u'File was empty')])
    name=StringField('Name',validators=[DataRequired()])
    author=StringField('Author', validators=[DataRequired()])
    description=TextAreaField('Description', default='book description')
    submit=SubmitField('Submit')


class BookEditForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    author=StringField('Author', validators=[DataRequired()])
    description=TextAreaField('Description', default='book description')
    submit=SubmitField('Submit')