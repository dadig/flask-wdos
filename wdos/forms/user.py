from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,RadioField,HiddenField
from wtforms.validators import DataRequired,Length

class CaseForm(FlaskForm):
    fayuan = StringField('法院',validators = ([DataRequired()]),render_kw = {})
    casenum = StringField('案号',validators = ([DataRequired()]),render_kw = {})
    yuangao = StringField('原告/申请人',validators = [DataRequired()],render_kw = {})
    beigao = StringField('被告/被执行人',validators = [DataRequired()],render_kw = {})
    lian_time = StringField('立案时间',render_kw = {})
    anyou  = StringField('案由',render_kw = {})
    biaodi = StringField('标的',render_kw = {})
    yuansheng_anhao = StringField('原审案号',render_kw = {})
    anjian_leibie = StringField('案件类别',render_kw = {})
    end_time = StringField('结案时间',render_kw = {})

    submit = SubmitField('保存')

class UserForm(FlaskForm):
    pass
    
class CreateDocumentsForm(FlaskForm):

    #choice = RadioField(' ',choices = [('value1','前期'),('value2',' 后期'),('value3','自选')])
    zxtzs = BooleanField('执行通知书')
    lzjdk = BooleanField('廉政监督卡')
    qlywgzs = BooleanField('权利义务告知书')

    submit = SubmitField('开始生成')
    


class test_document(FlaskForm):
    zxtzs = BooleanField('执行通知书',render_kw = {'id': 'zx'})
    hid = HiddenField('hide',render_kw = { 'id': '隐藏'})
    submit = SubmitField('submit')
