from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileRequired,FileField

from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length


class LoginForm(FlaskForm):
    username = StringField('Username',validators = [DataRequired()])
    password = PasswordField('Password',validators = [DataRequired(),Length(8,128)])
    remember = BooleanField('Remember me')

    submit = SubmitField('Login')

class TemplatesDocument(FlaskForm):
    templates = FileField('你的模板文件（为docx文件)',validators = [FileRequired('模板未选择'),FileAllowed(['docx'],'只许.docx')]) 
    submit = SubmitField('上传模板')
