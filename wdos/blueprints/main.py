from flask import Blueprint,render_template

main_bp = Blueprint('main',__name__)

@main_bp.route('/')
def main_index():
    return render_template('index.html')
@main_bp.route('/<test>')
def main_test(test):
    return render_template('index.html',test = test)

@main_bp.route('/base')
def main_base():
    return render_template('base.html')

