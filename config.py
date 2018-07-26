import os

class Config(object):
    """
    Common configurations
    """
    DEBUG = True
    JSONIFY_PRETTYPRINT_REGULAR =True
    SECRET = os.getenv('SECRET')
    SECRET_KEY = os.getenv('SECRET_KEY ')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    host = os.getenv('DB_HOST')
    database_name = os.getenv('DB_NAME')
    user = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')



class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    DB_NAME = os.getenv('mydiarydb')

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False

class TestingConfig(Config):
    """
    Production configurations
    """
    DEBUG = True
    TESTING = True
    DB_NAME = os.getenv('testdb')

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing':TestingConfig
}
