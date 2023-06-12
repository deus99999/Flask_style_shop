from flask import Blueprint, render_template
from flask import flash, session, render_template, request, redirect, url_for
from admin.forms import TeamForm, ProductForm
from models import Team, Product, Category
from config import db
import os
from decorators import admin_required
from flask_login import login_required


admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@admin.route("/")
@login_required
@admin_required
def admin_page():
    return render_template("admin/admin_page.html")


@admin.route('/team_form', methods=['GET', 'POST'])
@admin_required
def team_form_submit():
    form = TeamForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        surname = form.surname.data
        position = form.position.data
        photo = form.photo.data
        if not os.path.exists(f"static/images/team/"):
            os.makedirs(f"static/images/team/")
        # photo_filename = secure_filename(photo.filename)
        photo_path = f'static/images/team/' + photo.filename

        photo.save(photo_path)
        team = Team(first_name=first_name, surname=surname, position=position, photo=photo_path)
        try:
            db.session.add(team)
            db.session.commit()
            return redirect(url_for('admin.team_form_submit'))
        except:
            return "Ошибка. Возможно не создана база данных"
        return redirect(url_for('home'))
    team = Team.query.all()
    return render_template('admin/team_form.html', form=form, team=team)


@admin.route('/delete_team_member', methods=['POST'])
@admin_required
def delete_team_member():
    if request.method == 'POST':
        team_member_id = request.form['team_member_id']
        team_member_to_delete = Team.query.get(team_member_id)
        Team.query.filter_by(id=team_member_to_delete.id).delete()
        db.session.delete(team_member_to_delete)
        db.session.commit()
        return redirect('team_form')


@admin.route("/edit_category", methods=['GET', 'POST'])
@admin_required
def add_category():
    form = ProductForm()
    if request.method == 'POST':
        title = request.form['title']
        category_image = request.files['category_image']
        if not os.path.exists(f"static/images/Categories/{title}"):
            os.makedirs(f"static/images/Categories/{title}")
        image_path = f'static/images/Categories/{title}/' + category_image.filename
        category_image.save(image_path)
        category = Category(title=title, image_path=image_path)
        try:
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('admin.add_category'))
        except:
            return "Ошибка. Возможно не создана база данных"

    if request.method == 'GET':
        categories = Category.query.all()
        return render_template("admin/edit_category.html", categories=categories)

    return render_template("admin/edit_category.html")


@admin.route('/delete_category', methods=['POST'])
@admin_required
def delete_category():
    if request.method == 'POST':
        category_id = request.form['id']
        category_to_delete = Category.query.get(category_id)
        Product.query.filter_by(category_id=category_to_delete.id).delete()
        db.session.delete(category_to_delete)
        db.session.commit()
        return redirect('edit_category')


# create products
@admin.route("/edit_items", methods=['POST', 'GET'])
@admin_required
def edit_items():
    if request.method == "POST":
        category_id = request.form['category']
        title = request.form['title']
        description = request.form['description']

        if Category:
            category = Category.query.get(category_id)

            # creating path for saving images
            if not os.path.exists(f"static/images/Categories/{category.title}"):
                os.makedirs(f"static/images/Categories/{category.title}")

            item_image1 = request.files['item_image1']
            item_image_path1 = f'static/images/Categories/{category.title}/' + item_image1.filename
            item_image1.save(item_image_path1)

            item_image2 = request.files['item_image2']
            item_image_path2 = f'static/images/Categories/{category.title}/' + item_image2.filename
            item_image2.save(item_image_path2)

            item_image3 = request.files['item_image3']
            item_image_path3 = f'static/images/Categories/{category.title}/' + item_image3.filename
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

            return redirect('edit_items')
        except:
            return "Неверные данные или не заполнены все поля"

    if request.method == 'GET':
        categories = Category.query.all()
        products = Product.query.all()
        return render_template("admin/add_items.html", categories=categories, products=products)
    return render_template("admin/add_items.html")


@admin.route('/delete_item', methods=['POST'])
@admin_required
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
        return redirect('edit_items')


def change_image_path(item_image, product, cat):
    item_image = item_image.split('/')
    print(item_image)
    item_image[3] = f"{cat.title}"
    print(item_image)
    item_image = "/".join(item_image)
    print(item_image)
    return item_image


@admin.route('/change_item/<int:product_id>', methods=['POST', 'GET'])
@admin_required
def change_item(product_id):
    product = Product.query.filter_by(id=product_id).first()

    if request.method == 'POST':
        form = ProductForm(formdata=request.form, obj=product)

        # get choice of categories
        categories = Category.query.all()
        form.category_id.choices = [(category.id, category.title) for category in categories]

        v = request.form.get('category_id')
        print(v)
        # get category name
        # category_id = request.form.get('category_id')
        # print(category_id)
        # cat = Category.query.filter_by(id=category_id).first()
        # print(cat.title)
        #
        #
        # # get image path from db
        # item_img_1 = product.item_image1
        # print(item_img_1)
        #
        # item_img_2 = product.item_image2
        # item_img_3 = product.item_image3
        #
        # item_image_path1 = change_image_path(item_img_1, product, cat)
        # item_image_path2 = change_image_path(item_img_2, product, cat)
        # item_image_path3 = change_image_path(item_img_3, product, cat)
        #
        # product.item_image1 = item_image_path1
        # product.item_image2 = item_image_path2
        # product.item_image3 = item_image_path3


        form.populate_obj(product)

        db.session.commit()

        #flash("Changes saved.")
        return render_template('admin/change_item.html', product=product, form=form)

    if request.method == 'GET':
        form = ProductForm(obj=product)
    return render_template('admin/change_item.html', product=product, form=form)


