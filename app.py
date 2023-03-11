from flask import Flask, render_template, request, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///categories.db'


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), primary_key=True)

    user_name = db.Column(db.String(100), primary_key=True, nullable=False)
    # price = db.Column(db.Integer, primary_key=False)
    phone_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.id  # title and id when searching


@app.route("/")
def index():
    return render_template("/index.html")


@app.route("/shop")
def shop():
    return render_template("/shop.html")


@app.route("/about")
def about():
    return render_template("/about.html")


@app.route("/contacts", methods=["POST", "GET"])
def contacts():
    if request.method == "POST":
        email = request.form['email']
        name = request.form['name']
        phone_number = request.form['phone_number']

        user = User(email=email, user_name=name, phone_number=phone_number)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect("/index.html")

        except:
            return "Ошибка. Возможно не создана база данных"
    else:
        return render_template("/contacts.html")


if __name__ == "__main__":
    app.run(debug=True)

