import time
from flask import Blueprint,render_template,url_for,flash,request,redirect
from werkzeug import secure_filename
from io import BytesIO

from wdos.extensions import mongo,User
from wdos.decorators import admin_required, permission_required
from wdos.forms.admin import LoginForm,TemplatesDocument,RegisterForm

from flask_login import login_user,login_required,logout_user,current_user
from flask_login import LoginManager

admin_bp = Blueprint('admin',__name__)

@admin_bp.route('/logout')
@login_required
def admin_logout():
    flash('工作辛苦了，再见'+current_user.username,'info')
    logout_user()
    return redirect(url_for('.admin_login'))


@admin_bp.route('/',methods = ['GET','POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('user.case'))
    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user_one = mongo.db.users.find_one({'username':username})

        if user_one !=None and password == user_one['password']:
            user = User()
            user.id = user_one['user_id']
            user.username = user_one['judge_name']
            login_user(user)

            flash('登录成功！欢迎'+user.username,'info')
            return redirect(url_for('user.case'))
        else:
            flash('用户名或密码不对！！','warning')

            return redirect(url_for('.admin_login'))
    return render_template('admin/login.html',form = form  )

@admin_bp.route('/uploads/',methods = ['GET','POST'])
@login_required
@admin_required
def admin_uploads():
    form  = TemplatesDocument()
    templates_all = mongo.db.templates.find({},{'context':0})
    if form.validate_on_submit():
        for f in request.files.getlist('templates'):
            filename = f.filename
            
            template_stream = BytesIO()
            f.save(template_stream)
            mongo.db.templates.insert({'filename':filename,'context':template_stream.getvalue()})
            template_stream.close()

        flash('模板上传完成!','success')

    return  render_template('admin/uploads.html',form = form,templates_all = templates_all)

@admin_bp.route('/settings')
@login_required
@admin_required
def admin_settings(filename):
    pass

@admin_bp.route('/admin')
@login_required
@admin_required
def admin_case():
    find  = mongo.db.case.find({},{'_id':0})
    return render_template('admin/admin_case.html',find = find )


@admin_bp.route('/delete/<filename>',methods = ['GET','POST'])
@login_required
@admin_required
def admin_delete(filename):
    delete_file = {'filename':filename}
    mongo.db.templates.delete_one(delete_file)
    flash(filename+ "delete success",'success')
    return redirect(url_for('.admin_uploads')) 

@admin_bp.route('/register',methods = ['GET','POST'])
@login_required
@admin_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        court_name = form.court_name.data
        department = form.department.data
        username = form.username.data
        password = form.password.data
        re_password = form.re_password.data
        judge_name = form.judge_name.data
        judge_friend0 = form.judge_friend0.data
        judge_friend1 = form.judge_friend1.data
        clerk = form.clerk.data
        user_phone_number = form.user_phone_number.data
        register_time = time.time()
        user_id = str(hash(str(register_time) + username))
        permission = []
        user_dict = {
            'court_name'         : court_name ,
            'department'         : department ,
            'username'           : username ,
            'password'           : password ,
            're_password'        : re_password ,
            'judge_name'         : judge_name ,
            'judge_friend0'      : judge_friend0 ,
            'judge_friend1'      : judge_friend1 ,
            'clerk'              : clerk ,
            'user_phone_number'  : user_phone_number,
            'register_time'      : register_time,
            'user_id'            : user_id ,
            'permission'         : permission 

            }
        x = mongo.db.users.insert(user_dict)
        flash('chenggon' ,'sucess')
        return 'sucess' 
    return render_template('/admin/register.html',form = form)
