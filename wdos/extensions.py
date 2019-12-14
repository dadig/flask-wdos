from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
from flask_login import LoginManager,UserMixin,current_user

bootstrap = Bootstrap()
mongo = PyMongo()
login_manager = LoginManager()

login_manager.login_view = 'admin.admin_login'
login_manager.login_message = '请先登录'

class User(UserMixin):
    def can(self,permission_name):
        user = mongo.db.users.find_one({'user_id':current_user.id})
        return permission_name in user['permission']  

    def is_admin(self):
        user = mongo.db.users.find_one({'user_id':current_user.id})
        return 'ADMINISTER' in user['permission']  



@login_manager.user_loader
def user_loader(user_id):
    user = User()
    find = mongo.db.users.find_one({'user_id':user_id})
    user.id = user_id
    user.username = find['judge_name']

    return user


