from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms import validators


class CreateUser(FlaskForm):
    login = StringField("Login: ", [
        validators.DataRequired("Please enter your Login.")

    ])
    password = StringField("Password: ", [
        validators.DataRequired("Please enter your Password.")

    ])

    email = StringField("Email: ", [
        validators.DataRequired("Please enter your Email.")

    ])
    lastname = StringField("Lastname: ", [
        validators.DataRequired("Please enter your Lastname.")

    ])

    firstname = StringField("Firstname: ", [
        validators.DataRequired("Please enter your Firstname.")

    ])

    submit = SubmitField("Save")


class EditUser(FlaskForm):
    login = StringField("Login: ", [
        validators.DataRequired("Please enter your Login.")

    ])
    password = StringField("Password: ", [
        validators.DataRequired("Please enter your Password.")

    ])

    email = StringField("Email: ", [
        validators.DataRequired("Please enter your Email.")

    ])
    lastname = StringField("Lastname: ", [
        validators.DataRequired("Please enter your Lastname.")

    ])

    firstname = StringField("Firstname: ", [
        validators.DataRequired("Please enter your Firstname.")

    ])

    submit = SubmitField("Save")