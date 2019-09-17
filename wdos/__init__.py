import os
from flask import Flask

from wdos.setting import config

from wdos.extensions import mongo

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

    app.register_blueprint(admin_bp,url_prefix = '/admin')
    app.register_blueprint(auth_bp,url_prefix = '/auth')
    app.register_blueprint(user_bp,url_prefix = '/user')


def register_extensions(app):
    mongo.init_app(app)
