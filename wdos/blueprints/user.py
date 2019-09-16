from flask import Blueprint,render_template

user_bp = Blueprint('user',__name__)

@user_bp.route('/user')
def user_main():
    return render_template('/user/index.html')
