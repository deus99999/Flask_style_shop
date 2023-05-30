from flask import Blueprint, render_template, flash, redirect, url_for, request
from config import app, db, login_manager
from models import User, Team, Product, Category
from auth.forms import RegistrationForm, LoginForm
from mail import send_email
from flask_login import login_required, current_user, logout_user, login_user


auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Adding user's information to db after checking form by validators without sending email
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    email = form.email.data
    username = form.username.data
    #phone_number=form.phone_number.data
    password = form.password.data
    if email and username and password:
        if form.validate_on_submit:
            user = User(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
            flash("A confirmation email has been sent to you by email.")
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit:
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user is not None and user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for('home'))
            flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    # if user confirmed his account via email
    if current_user.confirmed:
        return redirect(url_for('home'))

    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
        db.session.commit()
        print('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
        print('The confirmation link is invalid or has expired.')
    return redirect(url_for('home'))


@login_required
@app.route('/my_account')
def my_account():
    return render_template('my_account.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    #flash('You have been logged out.')
    return redirect(url_for('auth.login'))


@auth.before_app_request
def before_request():
    print(request.endpoint)
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))


# confirming an account via email
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('home'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm',
               user=current_user,
               token=token)
    flash('A new confirmation email has been sent to you by email.')
    print('A new confirmation email has been sent to you by email.')
    return redirect(url_for('home'))


