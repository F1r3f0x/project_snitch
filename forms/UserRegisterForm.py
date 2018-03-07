from project_snitch.models import Usuario
from project_snitch import app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, validators


class UserRegisterForm(FlaskForm):
    nombre = StringField('Nombre', [validators.DataRequired(message='Dato obligatorio.'),
                                    validators.Length(min=3, max=256, message='Largo debe ser entre 3 y 256.',)])
    email = StringField('Email', [validators.DataRequired(message='Dato obligatorio.'),
                                  validators.Length(min=6, max=256, message='Largo debe ser entre 6 y 256.')])
    password = PasswordField('Contraseña',
                             [validators.DataRequired(message='Dato obligatorio.'),
                              validators.length(min=5, message='Largo debe ser mayor o igual que 5.'),
                              validators.EqualTo('confirm',
                                                 message='Las contraseñas tienen que ser iguales.')])
    confirm = PasswordField('Confirmar Contraseña')

    if not app.config['DEBUG']:
        recaptcha = RecaptchaField()

    def validate_nombre(self, nombre):
        usuario = Usuario.query.filter_by(nombre=nombre.data).first()
        if usuario:
            raise validators.ValidationError('El nombre de usuario ya existe.')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise validators.ValidationError('El email ya existe.')
