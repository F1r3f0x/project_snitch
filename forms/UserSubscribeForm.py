from flask_wtf import FlaskForm
from wtforms import SubmitField, validators


class UserSubscribeForm(FlaskForm):
    sapear = SubmitField('Sapear', [validators.data_required()])
