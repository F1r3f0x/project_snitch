from app.models import Usuario
from app import app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, validators


class UserChangeProfile(FlaskForm):
    nombre = StringField('Nuevo Nombre', [validators.Length(min=3, max=256, message='Largo debe ser entre 3 y 256.',),
                                          validators.Optional()])
    email = StringField('Nuevo Email', [validators.Length(min=6, max=256, message='Largo debe ser entre 6 y 256.'),
                                        validators.Optional()])
    password = PasswordField('Nueva Contraseña',
                             [validators.length(min=5, message='Largo debe ser mayor o igual que 5.'),
                              validators.EqualTo('confirm',
                                                 message='Las contraseñas tienen que ser iguales.'),
                              validators.Optional()])
    confirm = PasswordField('Confirmar Nueva Contraseña')

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
