"""
    Punto de Entrada para desarrollo
"""
from sys import path as syspath
from os import getcwd

path = getcwd()
path = path.split('\\')
new_path = '\\'.join(path[:-1])

syspath.extend([new_path])

from app import app, routes, admin_views
application = app

if __name__ == "__main__":
    application.run(port=5000, debug=True)
