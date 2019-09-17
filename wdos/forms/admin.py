from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length


class LoginForm(FlaskForm):
    username = StringField('Username',validators = [DataRequired()])
    password = PasswordField('Password',validators = [DataRequired(),Length(8,128)])
    remember = BooleanField('Remember me')

    submit = SubmitField('Login')
