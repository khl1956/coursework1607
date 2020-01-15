from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms import validators
from wtforms.validators import NumberRange, DataRequired


class CreateProject(FlaskForm):
    name = StringField("Name: ", [
        validators.DataRequired("Please enter project Name.")

    ])
    description = StringField("Description: ", [
        validators.DataRequired("Please enter project Description.")

    ])


    countoffiles = IntegerField("Count Of Projects:: ",
                         validators=[NumberRange(min=0, message=">1"), DataRequired("Please enter your Count Of Projects:.")]
                         )
    reposytoty_id = IntegerField("Reposytory id: ", [
        validators.DataRequired("Please enter project Reposytory id.")

    ])
    submit = SubmitField("Save")


class EditProject(FlaskForm):
    name = StringField("Name: ", [
        validators.DataRequired("Please enter project Name.")

    ])
    description = StringField("Description: ", [
        validators.DataRequired("Please enter project Description.")

    ])

    countoffiles = IntegerField("Count Of Projects:: ",
                                validators=[NumberRange(min=0, message=">0"),
                                            DataRequired("Please enter your Count Of Projects:.")]
                                )

    submit = SubmitField("Save")