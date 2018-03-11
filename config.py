class Config(object):
    """
    Clase que almacena las variables de configuracion para el proyecto.
    """

    # DB Variables
    DB_HOST = 'example.net'
    DB_PORT = 3306
    DB_USER = 'user'
    DB_PASS = 'pass'
    DB_NAME = 'db_name'

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CHANGELOG_DIR = 'changelog.txt'

    MSEARCH_ENABLE = True

    # Cifra cookies, es requerida por ciertas librerias.
    SECRET_KEY = 'TU_PROPIA_CLAVE_SECRETA_AQUI'

    # Claves para Recpatcha
    RECAPTCHA_PUBLIC_KEY = 'CLAVE_RECAPTCHA_AQUI'
    RECAPTCHA_PRIVATE_KEY = 'Y_AQUI'

    MINIFY_PAGE = True
