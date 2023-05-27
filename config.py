from flask import Flask, flash, session, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, logout_user
from secret import password, SECRET_KEY, my_email, my_email_username
from flask_bootstrap import Bootstrap
# from mail import mail
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# email server
app.config['MAIL_SERVER'] = 'smtp.ukr.net'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = my_email
app.config['MAIL_PASSWORD'] = password
app.config['REAL_STYLE_MAIL_SUBJECT_PREFIC'] = '[REAL STYLE]'
app.config['REAL_STYLE_MAIL_SENDER'] = 'rudenkoalexey@ukr.net>'
app.config['FLASKY_ADMIN'] = my_email
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
# app.permanent_session_lifetime = datetime.timedelta(days=1)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
mail.init_app(app)

# administrator list
ADMINS = ['your-gmail-username@gmail.com']
