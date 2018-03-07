"""
    Generardor de texto buscable con legisladores preexistentes
    Patricio Labin Correa - 2017
    GPLv3
"""
from my_tools.funciones import get_texto_buscable
from project_snitch import db
from project_snitch.models import Legislador


def gen_buscable_legisladores():
    """
    Genera texto_buscable para legisladores en la base de datos.
    """

    legisladores = Legislador.query.all()

    for legislador in legisladores:
        texto_no_buscable = f'{legislador.primer_nombre} {legislador.segundo_nombre} {legislador.primer_apellido} {legislador.segundo_apellido}'
        legislador.texto_buscable = get_texto_buscable(texto_no_buscable)

    db.session.commit()

if __name__ == '__main__':
    gen_buscable_legisladores()
    print('ok')

