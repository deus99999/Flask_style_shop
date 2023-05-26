from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from config import db, SECRET_KEY
# from itsdangerous import TimedSerializer
# TimedJSONWebSignatureSerializer
#from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask import current_app
from config import SECRET_KEY, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_item = db.Column(db.String(100), nullable=False)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(100), nullable=False)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    products = db.relationship('Product', backref='category', lazy='dynamic')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    item_image1 = db.Column(db.String(255), nullable=False)
    item_image2 = db.Column(db.String(255), nullable=False)
    item_image3 = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.String(100), default=True) # Boolean
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)#, primary_key=True)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=False, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    #phone_number = db.Column(db.Integer, nullable=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def generate_confirmation_token(self, expiration=3600):
    #     s = Serializer(SECRET_KEY, expiration)
    #     # print(s)
    #     return s.dumps({'confirm': self.id})

    # def confirm(self, token):
    #     s = Serializer(SECRET_KEY)
    #     try:
    #         data = s.loads(token)
    #        # print("data:", data)
    #     except:
    #         return False
    #     if data.get('confirm') != self.id:
    #         return False
    #     self.confirmed = True
    #     db.session.add(self)
    #     return True
