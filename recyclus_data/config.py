"""Application configuration."""
from pathlib import Path

db_dir = Path('.').parent.resolve()


class Config(object):
    pass

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