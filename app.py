from flask import Flask, render_template, request, redirect, render_template_string, current_app, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_image_alchemy.storages import S3Storage
from PIL import Image
import io
import base64
import os
import logging


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['BASIC_AUTH_USERNAME'] = 'flaskadmin'
app.config['BASIC_AUTH_PASSWORD'] = 'flaskadmin'


basic_auth = BasicAuth()

storage = S3Storage()
storage.init_app(app)
s3_storage = S3Storage()
MEDIA_PATH = "/images/"

app.config['SECRET_KEY'] = 'qwerty12'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    # products = db.relationship('Product', backref='category', lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    in_stock = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(50), nullable=False)
#     phone_number = db.Column(db.Integer, nullable=False)


# admin = Admin(app, name='microblog', template_mode='bootstrap3')
# admin.add_view(ModelView(Category, db.session))
# admin.add_view(ModelView(Item, db.session))

@app.route("/add_category", methods=['GET', 'POST'])
def create_category():
    if request.method == 'POST':
        title = request.form['title']
        category_image = request.files['category_image']
        image_path = 'static/images/' + category_image.filename
        category_image.save(image_path)
        category = Category(title=title, image_path=image_path)
        try:
            db.session.add(category)
            db.session.commit()
            return redirect("/")
        except:
            return "Ошибка. Возможно не создана база данных"
    if request.method == 'GET':
        categories = Category.query.all()
        return render_template("/add_category.html", categories=categories)

    return render_template("/add_category.html")


@app.route('/delete_post', methods=['POST'])
def remove_category():
    if request.method == 'POST':
        category_id = request.form['id']
        category = Category.query.get(category_id)
        db.session.delete(category)
        db.session.commit()
        return redirect('/add_category')




@app.route('/admin')
@basic_auth.required
def secret_view():
    return render_template('admin.html')


@app.route("/")
def home():
    categories = Category.query.all()
    return render_template("/home.html", categories=categories)


@app.route("/shop")
def shop():
    return render_template("/shop.html")


@app.route("/about")
def about():
    return render_template("/about.html")


@app.route("/contacts", methods=["POST", "GET"])
def contacts():
    if request.method == "POST":
        # name = request.form['name']
        # email = request.form['email']
        # phone_number = request.form['phone_number']
        #
        # user = User(name=name, email=email, phone_number=phone_number)
        try:
            # db.session.add(user)
            # db.session.commit()
            return redirect("/home.html")
        except:
            return "Ошибка. Возможно не создана база данных"
    else:
        return render_template("/contacts.html")





@app.route("/add_clothes", methods=['POST', 'GET'])
def add_clothes():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        in_stock = request.form['is_in_stock']

        product = Product(title=title, description=description, price=price, in_stock=in_stock)
        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/')
        except:
            return "Неверные данные или не заполнены все поля"
    else:
        return render_template("add_clothes.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
