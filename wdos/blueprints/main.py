from flask import Blueprint,render_template,flash,redirect,url_for
from wdos.forms.user import CaseForm,CreateDocumentsForm,test_document


main_bp = Blueprint('main',__name__)

@main_bp.route('/',methods = ['POST','GET'])
def main_index():
    form = test_document()
    if form.validate_on_submit():
        value = form.hid.name
        return redirect(url_for('.main_index'))
        return value
    return render_template('index.html',form = form )

@main_bp.route('/<test>')
def main_test(test):
    return render_template('base.html',test = test)

@main_bp.route('/base')
def main_base():
    return render_template('index.html' )

