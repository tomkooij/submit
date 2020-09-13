from app import pycode
from app.models import categories

from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                     SelectField)
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SubmissionForm(FlaskForm):
    comment = StringField('Comment')
    submission_file = FileField(validators=[FileRequired('Bestand toevoegen is verplicht!'), FileAllowed(pycode, 'Alleen .py en .ipynb toegestaan!')])
    submission_category  = SelectField(u'Opgave: ', choices = categories, validators = [DataRequired()])
    submit = SubmitField('Submit')
