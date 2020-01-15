from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms import validators


class CreateQuery(FlaskForm):

    nameOfProject = StringField("nameOfProject: ", [validators.DataRequired("Please enter your nameOfProject.")])
    Expansion = StringField("Expansion: ", [validators.DataRequired("Please enter your Expansion.")])
    submit = SubmitField("Search")

