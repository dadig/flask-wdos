from flask import Blueprint,render_template,url_for,flash,request,redirect
from wdos.extensions import mongo
from werkzeug import secure_filename
from wdos.forms.admin import LoginForm,TemplatesDocument
from io import BytesIO


admin_bp = Blueprint('admin',__name__)

@admin_bp.route('/main',methods = ['GET','POST'])
def admin_main():
    form = LoginForm()
    if form.validate_on_submit():
        flash('login success')

    return render_template('admin/index.html',form = form  )

@admin_bp.route('/uploads/',methods = ['GET','POST'])
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

@admin_bp.route('/delete/<filename>')
def admin_delete(filename):
    delete_file = {'filename':filename}
    mongo.db.templates.delete_one(delete_file)
    flash(filename+ "delete success",'success')
    return  redirect(url_for('.admin_uploads'))

