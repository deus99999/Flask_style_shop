from flask_mail import Mail, Message
from config import app
from threading import Thread
from flask import Flask, flash, current_app, render_template, request, redirect, url_for

mail = Mail()


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['REAL_STYLE_MAIL_SUBJECT_PREFIC'] + subject,
                  sender=app.config['REAL_STYLE_MAIL_SENDER'], recipients=[to])
    print(msg)
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr