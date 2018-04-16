"""
    Punto de Entrada (Debug)
"""
import sys

sys.path.extend(['/opt/python/current'])
print(sys.path)

from app import app, routes, admin_views
application = app

if __name__ == "__main__":
    application.run(port=5000, debug=True)
