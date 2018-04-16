"""
    Script de Inicializacion
"""
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee
from flask_admin import Admin
from flask_htmlmin import HTMLMIN
from flask_msearch import Search

# Flask App
app = Flask(__name__)

# Configs
from app.config import Config
_config = Config()

# Lee credenciales desde variables de entorno
from os import environ
_config.DB_HOST = environ.get('SNITCH_DB_HOST')
_config.DB_PORT = environ.get('SNITCH_DB_PORT')
_config.DB_NAME = environ.get('SNITCH_DB_NAME')
_config.DB_USER = environ.get('SNITCH_DB_USER')
_config.DB_PASS = environ.get('SNITCH_DB_PASS')
_config.SECRET_KEY = environ.get('SNITCH_SECRET_KEY')
_config.RECAPTCHA_PUBLIC_KEY = environ.get('SNITCH_RECAPTCHA_PUBLIC_KEY')
_config.RECAPTCHA_PRIVATE_KEY = environ.get('SNITCH_RECAPTCHA_PRIVATE_KEY')
_config.SQLALCHEMY_DATABASE_URI = f'mysql://{_config.DB_USER}:{_config.DB_PASS}@{_config.DB_HOST}:{_config.DB_PORT}/{_config.DB_NAME}'

if app.config['DEBUG']:
    _config.DEBUG = True
else:
    _config.DEBUG = False

app.config.from_object(_config)

db = SQLAlchemy(app)

searcher = Search(app)

# Configuracion de Login
login = LoginManager(app)
login.login_view = 'login_usuario'
login.login_message = 'Necesitas ingresar al sistema para ver esta pagina.'
login.login_message_category = 'warning'

admin = Admin(app, template_mode='bootstrap3')

minifier = HTMLMIN(app)

ID_ADMIN = 1
ID_USER = 2
ID_EDITOR = 3

ID_SENADOR = 1
ID_DIPUTADO = 2
