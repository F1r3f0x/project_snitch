"""
    Patricio Labin Correa - 2017
    GPLv3
"""
import json


def get_partidos():
    """
    Obtiene los partidos de la lista de legisladores para quitar los duplicados y
    traducirlos a los partidos del sistema
    """
    file_legisladores = input('Direccion de archivo con lista:\n')
    nombre_archivo = input('Nombre archivo con partidos\n')

    with open(file_legisladores, 'r') as f:
        lista_legisladores = json.load(f)

    with open(f'../datos/{nombre_archivo}.txt', 'w', encoding='utf-8') as f:
        for legislador in lista_legisladores:
            f.write(f'{legislador["partido"]}\n')


if __name__ == '__main__':
    get_partidos()
