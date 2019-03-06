import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from .config import config_by_name
from .routes import blueprint
from .datastore import mongo


def create_app(config_name='development'):
    print('create app', config_name)

    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.config.from_object(config_by_name[config_name])
    app.config.from_pyfile('config.py', silent=True)
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    mongo.init_app(app)
    app.register_blueprint(blueprint, url_prefix='/api')

    print(f'**** recyclus_datastore [{config_name}] created')

    return app
