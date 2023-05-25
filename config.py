from flask import Flask, flash, session, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, logout_user
# from flask_login import LoginForm
from flask_bootstrap import Bootstrap
from secret import password, SECRET_KEY, my_email
from flask_bootstrap import Bootstrap

app = Flask(__name__)
SECRET_KEY = SECRET_KEY
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.permanent_session_lifetime = datetime.timedelta(days=1)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# email server
MAIL_SERVER = 'smtp.ukr.net'
MAIL_PORT = '465'
MAIL_USERNAME = my_email
MAIL_PASSWORD = password
MAIL_USE_TLS = False
MAIL_USE_SSL = True

REAL_STYLE_MAIL_SENDER = 'REAL_STYLE Admin <flasky@example.com>'
REAL_STYLE_MAIL_SUBJECT_PREFIC = '[REAL_STYLE]'

# administrator list
ADMINS = ['your-gmail-username@gmail.com']
