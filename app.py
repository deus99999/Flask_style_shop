
# app = Flask(__name__)
#from models import User

# migrate = Migrate(app, db)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
#my_app.config['BASIC_AUTH_USERNAME'] = 'flaskadmin'
# my_app.config['BASIC_AUTH_PASSWORD'] = 'flaskadmin'
from secret import password, SECRET_KEY, my_email

# app.permanent_session_lifetime = datetime.timedelta(days=1)
# login_manager = LoginManager()
from config import app, login_manager
from config import db
from views import home, admin_page, create_category, delete_category, delete_team_member, shop, \
    product_detail, show_products_of_category, about, contacts, add_items, delete_item, add_to_cart, \
    delete_from_cart, cart, clear#, register, confirm
#from auth.views import login, logout


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    #app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)
