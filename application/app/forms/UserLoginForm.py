from app import app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, validators


class UserLoginForm(FlaskForm):
    nombre = StringField('Nombre', [validators.DataRequired(message='Dato obligatorio.'),
                                    validators.Length(min=3, max=256, message='Largo debe ser entre 3 y 256.',)])
    password = PasswordField('Contraseña',
                             [validators.DataRequired(message='Dato obligatorio.'),])
    remember_me = BooleanField()

    if not app.config['DEBUG']:
        recaptcha = RecaptchaField()
