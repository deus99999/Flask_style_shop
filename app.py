from flask import flash, session, render_template, request, redirect, url_for
import os
# import login_manager
from flask_login import login_required, logout_user, current_user
# from flask_login import LoginForm
from forms import TeamForm, LoginForm, RegistrationForm
from mail import mail


# app = Flask(__name__)
# app.secret_key = "my_super_secret_key"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
#my_app.config['BASIC_AUTH_USERNAME'] = 'flaskadmin'
# my_app.config['BASIC_AUTH_PASSWORD'] = 'flaskadmin'

# app.permanent_session_lifetime = datetime.timedelta(days=1)
# login_manager = LoginManager()
# login_manager.init_app(app)
from config import app, login_manager
from models import User, Team, Product, Category
from config import db
# from my_app.forms import


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/team_form', methods=['GET', 'POST'])
def team_form_submit():
    form = TeamForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        surname = form.surname.data
        position = form.position.data
        photo = form.photo.data
        # photo_filename = secure_filename(photo.filename)
        photo_path = f'static/images/team/' + photo.filename
        print(photo.filename)
        print(photo_path)
        photo.save(photo_path)
        team = Team(first_name=first_name, surname=surname, position=position, photo=photo_path)
        try:
            db.session.add(team)
            db.session.commit()
            return redirect("/team_form")
        except:
            return "Ошибка. Возможно не создана база данных"
        return redirect(url_for('home'))
    team = Team.query.all()
    return render_template('team_form.html', form=form, team=team)


# admin = Admin(my_app, name='admin', template_mode='bootstrap3')
# admin.add_view(ModelView(Category, db.session))
# admin.add_view(ModelView(Product, db.session))
# admin.add_view(ModelView(Team, db.session))


@app.route("/admin_page")
def admin_page():
    return render_template("/admin/admin_page.html")


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


@app.route('/delete_category', methods=['POST'])
def delete_category():
    if request.method == 'POST':
        category_id = request.form['id']
        category_to_delete = Category.query.get(category_id)
        Product.query.filter_by(category_id=category_to_delete.id).delete()
        db.session.delete(category_to_delete)
        db.session.commit()
        return redirect('/edit_category')


@app.route('/team_form', methods=['POST'])
def delete_team_member():
    if request.method == 'POST':
        team_member_id = request.form['id']
        member_to_delete = Category.query.get(team_member_id)
        Product.query.filter_by(member_id=member_to_delete.id).delete()
        db.session.delete(member_to_delete)
        db.session.commit()
        return redirect('/team_form')


# Show all categories in home.html
@app.route("/")
def home():
    categories = Category.query.order_by(Category.id).all()
    return render_template("/home.html", categories=categories)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            load_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('home'))

        flash('Invalid username or password.')

    return render_template('/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))


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


@app.route("/add_items", methods=['POST', 'GET'])
def add_items():
    if request.method == "POST":
        category_id = request.form['category']
        title = request.form['title']
        description = request.form['description']

        if Category:
            category = Category.query.get(category_id)

            # creating path for saving images
            if not os.path.exists(f"static/images/{category.title}"):
                os.makedirs(f"static/images/{category.title}")

            item_image1 = request.files['item_image1']
            item_image_path1 = f'static/images/{category.title}/' + item_image1.filename
            item_image1.save(item_image_path1)

            item_image2 = request.files['item_image2']
            item_image_path2 = f'static/images/{category.title}/' + item_image2.filename
            item_image2.save(item_image_path2)

            item_image3 = request.files['item_image3']
            item_image_path3 = f'static/images/{category.title}/' + item_image3.filename
            item_image3.save(item_image_path3)
        else:
            return "You should create category!"
        price = request.form['price']
        in_stock = request.form['is_in_stock']
        product = Product(category_id=category_id, title=title,
                          description=description,
                          item_image1=item_image_path1,
                          item_image2=item_image_path2,
                          item_image3=item_image_path3,
                          price=price, in_stock=in_stock)

        try:
            db.session.add(product)
            db.session.commit()

            return redirect('/add_items')
        except:
            return "Неверные данные или не заполнены все поля"

    if request.method == 'GET':
        categories = Category.query.all()
        products = Product.query.all()

        return render_template("/add_items.html", categories=categories, products=products)

    return render_template("/add_items.html")


@app.route('/delete_item', methods=['POST'])
def delete_item():
    if request.method == 'POST':
        item_id = request.form['item_id']
        # print(item_id)
        item_to_delete = Product.query.get(item_id)

        try:
            os.remove(item_to_delete.item_image1)
            os.remove(item_to_delete.item_image2)
            os.remove(item_to_delete.item_image3)
        except FileNotFoundError:
            print("There are no image with this name for removing")

        Product.query.filter_by(id=item_id).delete()
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/add_items')


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        mail.send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('home'))
    return render_template('/register.html', form=form)


@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('home'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('home'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
    # app.run(host='0.0.0.0', debug=True)
