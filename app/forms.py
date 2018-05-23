from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('user name', validators=[DataRequired('need something here')])
    password = PasswordField('password', validators=[DataRequired('need something here')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')
