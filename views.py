from flask import flash, session, render_template, request, redirect, url_for
import os
#from forms import LoginForm, RegistrationForm
from mail import send_email
from models import User, Team, Product, Category
from config import app, db, login_manager
from flask_login import login_required, current_user, logout_user, login_user


# admin = Admin(my_app, name='admin', template_mode='bootstrap3')
# admin.add_view(ModelView(Category, db.session))
# admin.add_view(ModelView(Product, db.session))
# admin.add_view(ModelView(Team, db.session))


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


@app.route("/<int:product_id>")
def product_detail(product_id):
    product = Product.query.filter_by(id=product_id).first()
    return render_template("/product_detail.html", product=product)


# Show all products of category in show.html
@app.route('/categories/<int:category_id>/products')
def show_products_of_category(category_id):
    category = Category.query.get_or_404(category_id)
    products = category.products
    return render_template('products_of_category.html', category=category, products=products)


@app.route("/about")
def about():
    team = Team.query.all()
    return render_template("/about.html", team=team)


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


# Код для добавления товара в корзину
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    products = Product.query.filter_by(id=product_id).all()
    session.permanent = True
    for product in products:
        if 'cart' not in session:
            session['cart'] = {}
        if str(product_id) not in session['cart']:
            session['cart'][str(product_id)] = {
                'title': product.title,
                'price_for_one': float(product.price),
                'price': float(product.price),
                'quantity': 1,
                'img_path': product.item_image1,
            }
        else:
            session['cart'][str(product_id)]['price'] += float(product.price)
            session['cart'][str(product_id)]['quantity'] += 1
            session.modified = True
            flash('Product was added to cart!')
    return redirect(request.referrer)


@app.route('/cart/<int:product_id>')
def delete_from_cart(product_id):
    cart_items = session.get('cart')
    cart_items.pop(str(product_id))
    session.modified = True
    return redirect(request.referrer)


@app.route('/cart')
def cart():
    all_products = Product.query.all()
    existing_titles = [one_product.title for one_product in all_products]  # titles of products that are in db

    cart_items = session.get('cart')
    total_cost = 0
    products = []
    if cart_items:
        for product_id, item in cart_items.items():
            product_dict = {
                'product_id': product_id,
                'title': item['title'],
                'price_for_one': item['price_for_one'],
                'price': item['price'],
                'quantity': item['quantity'],
                'item_image_path': item['img_path'],
                }

            products.append(product_dict)
            total_cost += item['price']

        # remove product from cart if product not in db
        for product_identity in cart_items.copy():
            product_dict = (cart_items[product_identity])
            product_title = (product_dict['title'])
            if product_title not in existing_titles:
                cart_items.pop(product_identity)
        session.modified = True

        return render_template('cart.html', products=products, total_cost=total_cost)
    else:
        return render_template('/cart.html')


@app.route("/cl")
def clear():
    session.clear()
    return "Session was cleared"






