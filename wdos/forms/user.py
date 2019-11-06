from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,RadioField,HiddenField,SelectField,TextField
from wtforms.validators import DataRequired,Length

class CaseForm(FlaskForm):
    case_number = StringField('案号',validators = ([DataRequired()]),render_kw = {})
    case_cause  = StringField('案由',validators = ([DataRequired()]),render_kw = {})
    case_subject_matter = StringField('标的',validators = ([DataRequired()]),render_kw = {})
    case_start_time = StringField('立案时间',render_kw = {})
    original_case_number = StringField('原审案号',render_kw = {})
    judgement_content = TextField('判决内容/执行目的',render_kw = {})
    judgement_time = StringField('判决时间',render_kw = {})
    case_end_cause = StringField('结案原因',render_kw = {})
    case_end_time = StringField('结案时间',render_kw = {})

    submit = SubmitField('保存')

class UserForm(FlaskForm):
    pass
    
class ClientForm(FlaskForm):
    client_c_d = SelectField(
            label = '案件类型',
            validators = ([DataRequired('申请人还是被执行人要分清')]),
            render_kw = {},
            choices  = [('申请人','申请人'),('被执行人','被执行人')],
            default  = '申请人'
            )
    client_name = StringField('名字',validators = ([DataRequired('要个当事人名字')]),render_kw = {})
    client_sex  = SelectField(
            label = '性别',
            validators = ([DataRequired('请选择性别')]),
            render_kw = {},
            choices = [('男','男'),('女','女')],
            default = '男'

            )
    client_ymd  = StringField('出生日期',validators = ([DataRequired()]),render_kw = {})
    client_address  = StringField('住址',validators = ([DataRequired()]),render_kw = {})
    client_id  = StringField('身份证号',render_kw = {})
    client_phone_number  = StringField('手机号码',render_kw = {})

    submit = SubmitField('保存')

class DocumentsForm(FlaskForm):
    pass
class CreateDocumentsForm(FlaskForm):
    pass

    #choice = RadioField(' ',choices = [('value1','前期'),('value2',' 后期'),('value3','自选')])
    zxtzs = BooleanField('执行通知书')
    lzjdk = BooleanField('廉政监督卡')
    qlywgzs = BooleanField('权利义务告知书')

    submit = SubmitField('开始生成')
    


class test_document(FlaskForm):
    zxtzs = BooleanField('执行通知书',render_kw = {'id': 'zx'})
    hid = HiddenField('hide',render_kw = { 'id': '隐藏'})
    submit = SubmitField('submit')
