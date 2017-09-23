import os

class Config(object):
    """Parent configuration class"""
    DEBUG = False

class DevelopmentConfig(Config):
    """Configuration for development"""
    DEBUG = True


class ProductionConfig(Config):
    """Configuration for production"""
    DATABASE_URI = 'mysql://user@localhost/foo'

app_config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
