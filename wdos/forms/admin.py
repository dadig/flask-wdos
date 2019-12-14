from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileRequired,FileField

from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField
from wtforms.validators import DataRequired,Length


class LoginForm(FlaskForm):
    username = StringField('用户名',validators = [DataRequired(),Length(1,20)])
    password = PasswordField('密码',validators = [DataRequired(),Length(1,20)])
    remember = BooleanField('记着我（下次可以直接登录）')

    submit = SubmitField('登录')

class TemplatesDocument(FlaskForm):
    templates = FileField('你的模板文件（为docx文件)',validators = [FileRequired('模板未选择'),FileAllowed(['docx'],'只许.docx')]) 
    submit = SubmitField('上传模板')


class RegisterForm(FlaskForm):
    #user_id
    #user_permission
    court_name  = SelectField(
            label = '法院名称:',
            validators = ([DataRequired('请选择法院名称')]),
            render_kw = {},
            choices = [('榆林市横山区人民法院','榆林市横山区人民法院')],
            default = '榆林市横山区人民法院'
            )

    department  = SelectField(
            label = '部门名称:',
            validators = ([DataRequired('请选择部门')]),
            render_kw = {},
            choices = [('执行庭','执行庭'),('民事审判庭','民事审判庭')],
            default = '执行庭'
            )

    username = StringField('用户名称:',validators = [DataRequired(),Length(3,20)])
    password = PasswordField('密码:',validators = [DataRequired(),Length(3,20)])
    re_password = PasswordField('再输一次密码:',validators = [DataRequired(),Length(3,20)])
    judge_name = StringField('法官名称/审判长:',validators = [DataRequired(),Length(1,20)])
    judge_friend0 = StringField('审判员(合议庭组成人员)')
    judge_friend1 = StringField('审判员(合议庭组成人员)')
    clerk = StringField('书记员:',validators = [DataRequired(),Length(1,20)])
    user_phone_number = StringField('电话：')

    submit = SubmitField('注册')
