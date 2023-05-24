import os
# import login_manager
# from flask_login import LoginForm
from secret import password, my_email, SECRET_KEY

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    REAL_STYLE_MAIL_SUBJECT_PREFIX = ['Real Style for Men']
    REAL_STYLE_MAIL_SENDER = 'Real Style Admin <mail@example.com>'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # email server
    MAIL_SERVER = 'smtp.ukr.net'
    MAIL_PORT = '465'
    MAIL_USERNAME = my_email
    MAIL_PASSWORD = password
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # administrator list
    ADMINS = ['your-gmail-username@gmail.com']


class TestingConfig(Config):
    Testing= True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data-test.db'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
    'production': ProductionConfig
}