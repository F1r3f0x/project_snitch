"""
    Punto de Entrada para desarrollo
"""
from app import app, routes, admin_views
application = app

if __name__ == "__main__":
    application.run(port=5000, debug=True)
