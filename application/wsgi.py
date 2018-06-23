# Entry point for webapp of Project Snitch
# F1r3f0x - 2018
from app import app, routes, admin_views

if __name__ == '__main__':
    app.run(port=5000)