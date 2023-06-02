from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError
from models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Keep me logged in', render_kw={"value": "Remember me"})
    submit = SubmitField('Log In', render_kw={"id": "submit"})


class RegistrationForm(FlaskForm):
    email = StringField('Your email', validators=[DataRequired(), Length(1, 64), Email()],
                        render_kw={"placeholder": "Email"})
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(1, 64),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must have only letters, '
                                              'numbers, dots or underscores')],
                           render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2',
                                                                             message='Passwords must match.')],
                             render_kw={"placeholder": "Password"})
    password2 = PasswordField('Confirm password', validators=[DataRequired()],
                              render_kw={"placeholder": "Confirm password"})

    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')