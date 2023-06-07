from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from config import app, db, SECRET_KEY
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config import SECRET_KEY, login_manager


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    # products = db.relationship('Product', backref='favorite_products')


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
    # favorites = db.relationship('Favorite', backref='products', lazy='dynamic')


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=False, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    #phone_number = db.Column(db.Integer, nullable=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    # role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # is_administrator = db.Column(db.Boolean, default=False)

    # def is_administrator(self):
    #     if self.
    #         return True

    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    #     if self.role is None:
    #         if self.email == app.config['ADMIN']:
    #             self.role = Role.query.filter_by(name='Administrator').first()  # if entered email of admin,
    #                                                                         # user get admins permissions
    #         if self.role is None:
    #             self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer((app.config['SECRET_KEY']), expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    # True, if user have all permissions
    # def can(self, permissions):
    #     print("can: ", self.role is not None and (self.role.permissions and permissions) == permissions)
    #     return self.role is not None and (self.role.permissions and permissions) == permissions

#     def is_administrator(self):
#         if self.can(Permission.ADMINISTER):
#             print("is admin true")
#             return True
#
#
# class AnonymousUser(AnonymousUserMixin):
#     def can(self, permissions):
#         return True
#
#     def is_administrator(self):
#         return False
#
#
# login_manager.anonymous_user = AnonymousUser
#
#
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#
#
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     default = db.Column(db.Boolean, default=False, index=True)
#     permissions = db.Column(db.Integer)
#     users = db.relationship('User', backref='role', lazy='dynamic')
#
#     @staticmethod
#     def insert_roles():
#         roles = {
#             'User': [Permission.FOLLOW, Permission.COMMENT],
#             'Moderator': [Permission.WRITE_ARTICLES],
#             'Administrator': (0xff, True)
#         }
#
#         # roles = {
#         #     'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
#         #     'Moderator': [Permission.FOLLOW, Permission.COMMENT,
#         #                   Permission.WRITE, Permission.MODERATE],
#         #     'Administrator': [Permission.FOLLOW, Permission.COMMENT,
#         #                       Permission.WRITE, Permission.MODERATE,
#         #                       Permission.ADMIN],
#         # }
#
#         for r in roles:
#             print(r)
#             role = Role.query.filter_by(name=r).first()
#             if role is None:
#                 role = Role(name=r)
#             role.permissions = roles[r][0]
#             role.default = roles[r][1]
#             db.session.add(role)
#         db.session.commit()
#
#
# class Permission:
#     FOLLOW = 0x01
#     COMMENT = 0x02
#     WRITE_ARTICLES = 0x04
#     MODERATE_COMMENTS = 0x08
#     ADMINISTER = 0x80
#
# # class Permission:
# #     FOLLOW = 1
# #     COMMENT = 2
# #     WRITE = 4
# #     MODERATE = 8
# #     ADMINISTER = 16
