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


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    item_image_path = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.String(100), default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True, nullable=False)

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
            return redirect("/add_category")
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
        category_to_delete = Category.query.get(category_id)
        Product.query.filter_by(category_id=category_to_delete.id).delete()
        db.session.delete(category_to_delete)
        db.session.commit()
        return redirect('/add_category')


# @app.route("/<int:product_id>")
# def product_detail(product_id):
#     product = Product.query.get_or_404(product_id)
#     return render_template("/item_detail.html", product=product)


@app.route('/admin')
@basic_auth.required
def secret_view():
    return render_template('admin.html')


# Show all categories in home.html
@app.route("/")
def home():
    categories = Category.query.order_by(Category.id).all()
    return render_template("/home.html", categories=categories)


# Show all products in show.html
@app.route("/shop")
def shop():
    products = Product.query.all()
    return render_template("shop.html", products=products)


@app.route('/<int:category_id>')
def show_products_of_category(category_id):
    products = Product.query.filter_by(category_id=category_id).all()
    return render_template('shop.html', products=products)


@app.route("/product_detail")
def product_detail():
    return render_template("/product_detail.html")


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


@app.route("/add_items", methods=['POST', 'GET'])
def add_items():
    if request.method == "POST":
        category_id = request.form['category']
        title = request.form['title']
        description = request.form['description']

        if Category:
            categories = Category.query.all()
            for category in categories:
                if not os.path.exists(f"static/images/{category.title}"):
                    os.makedirs(f"static/images/{category.title}")


                item_image = request.files['item_image']
                item_image_path = f'static/images/{category.title}/' + item_image.filename
        item_image.save(item_image_path)

        price = request.form['price']
        in_stock = request.form['is_in_stock']
        print(in_stock)
        product = Product(category_id=category_id, title=title,
                          description=description,
                          item_image_path=item_image_path,
                          price=price, in_stock=in_stock)

        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/add_items')
        except:
            return "Неверные данные или не заполнены все поля"

    if request.method == 'GET':
        categories = Category.query.all()
        return render_template("/add_items.html", categories=categories)

    return render_template("/add_items.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
