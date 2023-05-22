from flask import Flask, flash, session, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# import login_manager
from flask_login import LoginManager, login_required, logout_user
# from flask_login import LoginForm
from flask_bootstrap import Bootstrap

app = Flask(__name__)
SECRET_KEY = "my_super_secret_key"
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.permanent_session_lifetime = datetime.timedelta(days=1)
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'your-gmail-username'
MAIL_PASSWORD = 'your-gmail-password'

# administrator list
ADMINS = ['your-gmail-username@gmail.com']