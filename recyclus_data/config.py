"""Application configuration."""
import os
from pathlib import Path

db_dir = Path('.').parent.resolve()
user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

class Config(object):
    MONGO_URI = f'mongodb://{user}:{password}@datastore-db:27017/datastore?authSource=admin'


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True

    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)