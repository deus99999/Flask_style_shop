from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError
from models import User


class EditEmailForm(FlaskForm):
    email = StringField('Your new email', validators=[DataRequired(), Length(1, 64), Email()],
                        render_kw={"placeholder": "Your new email"})
    username = StringField('New username',
                           validators=[DataRequired(),
                                       Length(1, 64),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must have only letters, '
                                              'numbers, dots or underscores')],
                           render_kw={"placeholder": "New username"})
    submit = SubmitField('Change email')


class EditUsernameForm(FlaskForm):
    username = StringField('New username',
                           validators=[DataRequired(),
                                       Length(1, 64),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must have only letters, '
                                              'numbers, dots or underscores')],
                           render_kw={"placeholder": "New username"})
    submit = SubmitField('Change username')





class FavoriteForm(FlaskForm):
    in_favorites = BooleanField()

# class RegistrationForm(FlaskForm):
#     email = StringField('Your email', validators=[DataRequired(), Length(1, 64), Email()],
#                         render_kw={"placeholder": "Email"})
#     username = StringField('Username',
#                            validators=[DataRequired(),
#                                        Length(1, 64),
#                                        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
#                                               'Usernames must have only letters, '
#                                               'numbers, dots or underscores')],
#                            render_kw={"placeholder": "Username"})
#     password = PasswordField('Password',
#                              validators=[DataRequired(),
#                                          EqualTo('password2',
#                                                  message='Passwords must match.')],
#                              render_kw={"placeholder": "Password"})
    # password2 = PasswordField('Confirm password',
    #                           validators=[DataRequired()],
    #                           render_kw={"placeholder": "Confirm password"})
    # submit = SubmitField('Register')
    #
    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError('Email already registered.')
    #
    # def validate_username(self, field):
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('Username already in use.')



