from config import app, mail, Message
from flask import Flask, flash, current_app, render_template, request, redirect, url_for
from threading import Thread
from celery import Celery


# Set up celery client
client = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
client.conf.update(app.config)


@client.task
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['REAL_STYLE_MAIL_SUBJECT_PREFIC'] + subject,
                  sender=app.config['REAL_STYLE_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
