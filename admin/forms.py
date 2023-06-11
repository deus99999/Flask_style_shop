from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class TeamForm(FlaskForm):
    first_name = StringField("Name: ", validators=[DataRequired()])
    surname = StringField("Surname: ", validators=[DataRequired()])
    position = StringField("Position: ", validators=[DataRequired()])
    photo = FileField('Photo: ', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])


class ProductForm(FlaskForm):
    category_id = StringField(validators=[DataRequired()])
    title = StringField("title: ", validators=[DataRequired()])
    description = TextAreaField ("description: ", validators=[DataRequired()])
    item_image1 = FileField('Main photo: ', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    item_image2 = FileField('Photo: ', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    item_image3 = FileField('Photo: ', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    price = StringField(validators=[DataRequired()])
    in_stock = BooleanField('Is this in stock:', render_kw={"value": "Remember me"})
