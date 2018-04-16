from flask_wtf import FlaskForm
from wtforms import SubmitField, validators


class UserUnsubscribeForm(FlaskForm):
    dejar = SubmitField('Dejar de Sapear', [validators.data_required()])
