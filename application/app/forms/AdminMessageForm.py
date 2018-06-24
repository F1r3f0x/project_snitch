from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators


class AdminMessageForm(FlaskForm):
    titulo = StringField('Titulo', [validators.DataRequired(message='Campo obligatorio.'),
                                    validators.Length(min=3, max=512, message='Largo debe ser entre 3 y 256.',)])
    contenido = TextAreaField('Contenido',
                              [
                                  validators.DataRequired(message='Campo obligatorio'),
                                  validators.Length(min=3, max=2048, message='Largo debe ser entre 3 y 2048',)
                              ])
