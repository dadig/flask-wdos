from flask import Blueprint,render_template
from wdos.extensions import mongo


auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/auth')
def auth_main():
    one = mongo.db.run.find()

    return one[0]['time'] + one[1]['测试']

@auth_bp.route('/<t>')
def auth_t(t):
    return  render_template('auth/index.html',t = t)
