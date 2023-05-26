from flask import Flask, flash, session, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, logout_user
# from flask_login import LoginForm
from flask_bootstrap import Bootstrap
from secret import password, SECRET_KEY, my_email, my_email_username
from flask_bootstrap import Bootstrap
# from mail import mail
from flask_mail import Mail, Message

app = Flask(__name__)
SECRET_KEY = SECRET_KEY
app.secret_key = SECRET_KEY
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
app.config['REAL_STYLE_MAIL_SENDER'] = 'REAL_STYLE_Admin <rudenkoalexey@ukr.net>'
app.config['FLASKY_ADMIN'] = my_email
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
# app.permanent_session_lifetime = datetime.timedelta(days=1)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)



bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
mail.init_app(app)



def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['REAL_STYLE_MAIL_SUBJECT_PREFIC'] + subject,
                  sender='rudenkoalexey@ukr.net',
    #app.config['REAL_STYLE_MAIL_SENDER']
                  recipients=[to])
    print(msg)
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    print(msg.html)
    mail.send(msg)


# administrator list
ADMINS = ['your-gmail-username@gmail.com']
