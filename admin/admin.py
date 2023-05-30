from flask import Blueprint, render_template
from flask import flash, session, render_template, request, redirect, url_for
from admin.forms import TeamForm
from models import Team, Product, Category
from config import db
import os


admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@admin.route("/")
def admin_page():
    return render_template("admin/admin_page.html")


@admin.route('/team_form', methods=['GET', 'POST'])
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
        print(photo.filename)
        print(photo_path)
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
def delete_team_member():
    if request.method == 'POST':
        team_member_id = request.form['team_member_id']
        team_member_to_delete = Team.query.get(team_member_id)
        Team.query.filter_by(id=team_member_to_delete.id).delete()
        db.session.delete(team_member_to_delete)
        db.session.commit()
        return redirect('team_form')


@admin.route("/edit_category", methods=['GET', 'POST'])
def add_category():
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
def delete_category():
    if request.method == 'POST':
        category_id = request.form['id']
        category_to_delete = Category.query.get(category_id)
        Product.query.filter_by(category_id=category_to_delete.id).delete()
        db.session.delete(category_to_delete)
        db.session.commit()
        return redirect('edit_category')


@admin.route("/edit_items", methods=['POST', 'GET'])
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
