from flask import flash, session, render_template, request, redirect, url_for, abort
from models import Team, Product, Category, Favorite, User
from config import app, db
from flask_login import current_user, login_required
from forms import EditEmailForm, EditUsernameForm
from config import Api, Checkout


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

        return render_template('/cart.html', products=products, total_cost=total_cost)
    else:
        return render_template('/cart.html')


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


@app.route('/add_quantity_to_cart/<int:product_id>')
def add_quantity_to_cart(product_id):
    products = Product.query.filter_by(id=product_id).all()
    session.permanent = True
    for product in products:
        session['cart'][str(product_id)]['price'] += float(product.price)
        session['cart'][str(product_id)]['quantity'] += 1
        session.modified = True
    return redirect(request.referrer)


# delete quantity of product from cart
@app.route('/delete_quantity_from_cart/<int:product_id>')
def delete_quantity_from_cart(product_id):
    products = Product.query.filter_by(id=product_id).all()
    session.permanent = True
    for product in products:
        if session['cart'][str(product_id)]['quantity'] > 1:
            session['cart'][str(product_id)]['price'] -= float(product.price)
            session['cart'][str(product_id)]['quantity'] -= 1
            session.modified = True
    return redirect(request.referrer)


# delete all quantity of product from card
@app.route('/cart/<int:product_id>')
def delete_from_cart(product_id):
    cart_items = session.get('cart')
    cart_items.pop(str(product_id))
    session.modified = True
    return redirect(request.referrer)


# Show all products of category in show.html
@app.route('/categories/<int:category_id>/products')
def show_products_of_category(category_id):
    category = Category.query.get_or_404(category_id)
    products = category.products
    return render_template('products_of_category.html', category=category, products=products)


@app.route("/<int:product_id>")
def product_detail(product_id):
    product = Product.query.filter_by(id=product_id).first()
    print(product.id)

    if current_user.is_authenticated:
        favorite_list = get_favorite_list()
        favorite_list = [fav.id for fav in favorite_list]
        return render_template("/product_detail.html", product=product, favorite_list=favorite_list)
    else:
        if session.get('favorite'):
            favorite_items = session.get('favorite')
            print(favorite_items)
            favorites_id_list = [int(product_id) for product_id in favorite_items]
            return render_template("/product_detail.html", product=product, favorites_id_list=favorites_id_list)

    return render_template("/product_detail.html", product=product)


def get_favorite_list():
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    favorite_list = []
    for favorite in favorites:
        product = Product.query.filter_by(id=favorite.product_id).first()
        favorite_list.append(product)
    print(favorite_list)
    return favorite_list


@app.route("/favorite")
def favorite():
    if not current_user.is_authenticated:
        all_products = Product.query.all()
        existing_titles = [one_product.title for one_product in all_products]  # titles of products that are in db
        favorite_items = session.get('favorite')
        products = []
        if favorite_items:
            for product_id, item in favorite_items.items():
                product_dict = {
                    'product_id': product_id,
                    'title': item['title'],
                    'price': item['price'],
                    'item_image_path': item['img_path'],
                    }

                products.append(product_dict)

            # remove product from favorite if product not in db
            for product_identity in favorite_items.copy():
                product_dict = (favorite_items[product_identity])
                product_title = (product_dict['title'])
                if product_title not in existing_titles:
                    favorite_items.pop(product_identity)
            session.modified = True
            return render_template('/favorite.html', products=products)

    if current_user.is_authenticated:
        favorite_list = get_favorite_list()
        return render_template('/favorite.html', favorite_list=favorite_list)
    return render_template('/favorite.html')


@app.route("/add_to_favorites/<int:product_id>")
def add_to_favorites(product_id):
    if not current_user.is_authenticated:
        products = Product.query.filter_by(id=product_id).all()
        session.permanent = True
        for product in products:
            # if product.id in session['favorite']:
            #     flash('Product is already in favorites.')
            if 'favorite' not in session:
                session['favorite'] = {}
            if str(product_id) not in session['favorite']:
                session['favorite'][str(product_id)] = {
                    'title': product.title,
                    'price': float(product.price),
                    'img_path': product.item_image1,
                }
                session.modified = True
                flash('Product was added to favorite!')
                print('Product was added to favorite!')
            return redirect(request.referrer)

    if current_user.is_authenticated:
        favorites = Favorite(user_id=current_user.id, product_id=product_id)
        print(favorites.user_id)

        # check product in Favorite
        favorite_exists = Favorite.query.filter_by(user_id=current_user.id, product_id=product_id).first()

        if not favorite_exists:
            db.session.add(favorites)
            try:
                db.session.commit()
                flash('Product was added to favorite!')
                print('Product was added to favorite!')
            except:
                print('Error.')
            return redirect(request.referrer)
    return redirect(request.referrer)


@app.route('/delete_from_favorites/<int:product_id>')
def delete_from_favorites(product_id):
    if not current_user.is_authenticated:
        favorite_items = session.get('favorite')
        favorite_items.pop(str(product_id))
        session.modified = True
        flash('Product was removed from favorite!')

    if current_user.is_authenticated:
        favorite_to_delete = Favorite.query.filter_by(user_id=current_user.id).filter_by(product_id=product_id).first()
        print("favorite_to_delete", favorite_to_delete)
        if favorite_to_delete:
            db.session.delete(favorite_to_delete)
            db.session.commit()
    return redirect(request.referrer)


@app.route("/my_account")
def my_account():
    return render_template('/my_account.html')


@app.route('/edit_email', methods=['GET', 'POST'])
@login_required
def edit_email():
    form = EditEmailForm()

    if form.email.data:
        if form.validate_on_submit:
            new_email = form.email.data
            existing_user = User.query.filter_by(email=new_email).first()

            if existing_user and existing_user.id != current_user.id:
                flash("This email is already exist.")
            else:
                current_user.email = new_email
                db.session.commit()
                flash("Your email has been updated.")

            return redirect(url_for('edit_email'))
    form.email.data = current_user.email
    return render_template("edit_email.html", form=form)


@app.route('/edit_username', methods=['GET', 'POST'])
@login_required
def edit_username():
    form = EditUsernameForm()

    if form.username.data:
        if form.validate_on_submit:
            new_username = form.username.data
            existing_user = User.query.filter_by(email=new_username).first()

            if existing_user and existing_user.id != current_user.id:
                flash("This username is already exist.")
            else:
                current_user.username = new_username
                db.session.commit()
                flash("Your username has been updated.")

            return redirect(url_for('edit_username'))
    form.username.data = current_user.username
    return render_template("edit_username.html", form=form)


@app.route('/buy/<int:total_cost>')
def buy(total_cost):
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": str(total_cost) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/buy_now/<int:price>')
def buy_now(price):
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": str(price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route("/cl")
def clear():
    session.clear()
    return "Session was cleared"






