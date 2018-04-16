"""
    Punto de Entrada (Debug)
"""
from app import app
from app import routes, admin_views

if __name__ == "__main__":
    app.run(port=5000, debug=True)
