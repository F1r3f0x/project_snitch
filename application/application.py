"""
    Punto de Entrada para AWS Elastic Beanstalk
"""
from app import app, routes, admin_views
application = app

if __name__ == "__main__":
    application.run(port=5000)
