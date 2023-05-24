#!/usr/bin/env python

import os
from . import db, create_app
from models import User, Team, Product, Category
from flask_script import Manager, Shell
from flask_migrate import Migrate


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app)


@manager.command
def test():
    """run module tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


def make_shell_context():
    return dict(app=app, db=db, User=User, Team=Team, Product=Product, Category=Category)


manager.add_command("shell", Shell(make_context=make_shell_context()))
manager.add_command('db')


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()

    manager.run()
    # app.run(host='0.0.0.0', debug=True)