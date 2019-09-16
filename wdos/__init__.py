from flask import Flask
from wdos.extensions import mongo

def create_app():

    app = Flask('wdos')

    app.config.update(MONGO_URI = 'mongodb://localhost:27017/test')


    mongo.init_app(app)



    from wdos.blueprints.main import main_bp
    from wdos.blueprints.admin import admin_bp
    from wdos.blueprints.auth import auth_bp
    from wdos.blueprints.user import user_bp


    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp,url_prefix = '/admin')
    app.register_blueprint(auth_bp,url_prefix = '/auth')
    app.register_blueprint(user_bp,url_prefix = '/user')

    return app
