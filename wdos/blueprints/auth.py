from flask import Blueprint,render_template
from wdos.extensions import mongo


auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/auth')
def auth_main():
    one = mongo.db.run.find()

    return one[0]['time']
