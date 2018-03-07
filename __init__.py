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

# Flask App
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

#whooshee = Whooshee(app)
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