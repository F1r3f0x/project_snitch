"""
    Punto de Entrada (Debug)
"""
from project_snitch import app

if __name__ == "__main__":
    app.run(port=5000, threaded=True, debug=True)
