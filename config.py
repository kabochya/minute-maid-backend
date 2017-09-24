import os

class Config(object):
    """Parent configuration class"""
    DEBUG = False
    BUCKET_ID = "xxnet-172504.appspot.com"
    PROJECT_ID = "xxnet-172504"
    MONGO_DBNAME = 'mhacks'
    MONGO_URI = 'mongodb://localhost:27017/mhacks'

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
