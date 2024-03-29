import os
from flask import Flask
import flask_login

from wdos.setting import config

from wdos.extensions import mongo,bootstrap,login_manager
from wdos.utils import is_banjiao,str_client,ishan,c_d_list

from wdos.blueprints.main import main_bp
from wdos.blueprints.admin import admin_bp
from wdos.blueprints.auth import auth_bp
from wdos.blueprints.user import user_bp

def create_app( config_name = None ):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG','development')

    app = Flask('wdos')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)

    return app

def register_blueprints(app):
    app.register_blueprint(main_bp)

    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp,url_prefix = '/auth')
    app.register_blueprint(user_bp,url_prefix = '/user')


def register_extensions(app):
    bootstrap.init_app(app)
    mongo.init_app(app)
    login_manager.init_app(app)


