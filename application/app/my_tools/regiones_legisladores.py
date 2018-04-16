"""
    Patricio Labin Correa - 2017
    GPLv3
"""
import json
import datetime


def get_regiones():
    """
        Obtiene las regiones de la lista de legisladores para quitar los
        duplicados y traducirlos a las regiones del sistema
    """
    file_legisladores = input('Direccion archivo legisladores:\n')
    nombre_archivo = input('Nombre archivo con regiones:\n')

    with open(file_legisladores, 'r') as f:
        dict_legisladores = json.load(f)

        print(dict_legisladores)

    with open(f'../datos/{nombre_archivo}.txt', 'w', encoding='utf-8') as f:
        for legislador in dict_legisladores:
            f.write(f'{legislador["region"]}\n')


if __name__ == '__main__':
    get_regiones()
