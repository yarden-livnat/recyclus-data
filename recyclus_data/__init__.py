import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from .config import config_by_name
from .routes import blueprint
from .datastore import mongo


def create_app(config_name='production'):
    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.config.from_object(config_by_name[config_name])
    app.config.from_pyfile('config.py', silent=True)
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)

    mongo.init_app(app)
    app.register_blueprint(blueprint, url_prefix='/api')

    return app
