"""
    Agrega id de ultimo tipo de cargo a los legisladores en el sistema
    Patricio Labin Correa - 2018
    GPLv3
"""
from project_snitch import db
from project_snitch.models import Legislador, CargoLegislativo


def agregar_ultimo_cargo():
    """
    Genera texto_buscable para legisladores en la base de datos.
    """
    legisladores = Legislador.query.all()

    for legislador in legisladores:
        ultimo_cargo = CargoLegislativo.query.filter_by(legislador_id=legislador.id).order_by(CargoLegislativo.fecha_ingreso.desc()).all()[0]
        legislador.ultimo_tipo_legislador_id = ultimo_cargo.tipo.id

    db.session.commit()

if __name__ == '__main__':
    agregar_ultimo_cargo()
    print('ok')