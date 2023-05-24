from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from models import User


class TeamForm(FlaskForm):
    first_name = StringField("Name: ", validators=[DataRequired()])
    surname = StringField("Surname: ", validators=[DataRequired()])
    position = StringField("Position: ", validators=[DataRequired()])
    photo = FileField('Photo: ', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])