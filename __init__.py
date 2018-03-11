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

# Configs
from project_snitch.config import Config
_config = Config()

# Lee credenciales desde archivo
lineas = ''
with open('../credenciales.txt') as _f:
    lineas = _f.readlines()

_config.DB_HOST = lineas[0].strip()
_config.DB_PORT = lineas[1].strip()
_config.DB_NAME = lineas[2].strip()
_config.DB_USER = lineas[3].strip()
_config.DB_PASS = lineas[4].strip()
_config.SECRET_KEY = lineas[5].strip()
_config.RECAPTCHA_PUBLIC_KEY = lineas[6].strip()
_config.RECAPTCHA_PRIVATE_KEY = lineas[7].strip()
_config.SQLALCHEMY_DATABASE_URI = f'mysql://{_config.DB_USER}:{_config.DB_PASS}@{_config.DB_HOST}:{_config.DB_PORT}/{_config.DB_NAME}'

# Flask App
app = Flask(__name__)
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