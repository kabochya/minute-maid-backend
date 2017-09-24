import os

class Config(object):
    """Parent configuration class"""
    DEBUG = False
    BUCKET_ID = "mhacks-audio"
    PROJECT_ID = "celestial-tract-180903"
    MONGO_DBNAME = 'mhacks'
    MONGO_URI = 'mongodb://localhost:27017/mhacks'

class DevelopmentConfig(Config):
    """Configuration for development"""
    DEBUG = True


class ProductionConfig(Config):
    """Configuration for production"""
    DEBUG = False

app_config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
