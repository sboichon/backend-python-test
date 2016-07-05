class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'development key'
    USERNAME = 'admin'
    PASSWORD = 'default'


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = '/tmp/alayatodo.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE


class TestingConfig(Config):
    TESTING = True
    DATABASE = '/tmp/alayatodo_test.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
