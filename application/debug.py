"""
    Punto de Entrada para desarrollo
"""
from app import app, routes, admin_views
from sys import path as syspath
print(syspath)
application = app

if __name__ == "__main__":
    application.run(port=5000, debug=True)
