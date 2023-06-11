from views import home, shop, product_detail, show_products_of_category, about, contacts, buy
from config import app, db
from admin.admin import admin, add_category, delete_category
from auth.auth import auth

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(auth, url_prefix='/auth')


# @app.context_processor
# def inject_permissions():
#     return dict(Permission=Permission)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Role.insert_roles()

    # app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)
