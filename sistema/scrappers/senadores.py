"""
    Scrapper Senadores
    Patricio Labin Correa (F1r3f0x) - 2017
    GPLv3
"""
from datetime import datetime
from bs4 import BeautifulSoup
from requests import get as requests_get
from requests import exceptions as requests_exceptions


URL_LISTADO_SENADORES_VIGENTES = 'http://www.senado.cl/wspublico/senadores_vigentes.php'
TEMPLATE_URL_PEFIL_SENADOR = 'http://www.senado.cl/appsenado/index.php?mo=senadores&ac=fichasenador&id='

def get_lista_senadores():
    """
    Obtiene la lista de senadores con sus datos desde el servicio xml de senado.cl
    :return: lista_senadores
    :rtype: dict
    """
    lista_senadores = []
    try:
        page = requests_get(URL_LISTADO_SENADORES_VIGENTES)
    except (ConnectionError, ConnectionRefusedError,
            requests_exceptions.MissingSchema) as err:
        print(f'Error al obtener listado desde senado.cl {err}')
        return None

    soup = BeautifulSoup(page.content, 'xml')

    senadores_vigentes = soup.find_all('senador')
    for _senador in senadores_vigentes:
        id_interna = _senador.find('PARLID').text
        senador = {
            'tipo': 'Senador',
            'id_interna': id_interna,
            'link': f'{TEMPLATE_URL_PEFIL_SENADOR}{id_interna}',
            'primer_apellido': _senador.find('PARLAPELLIDOPATERNO').text,
            'segundo_apellido': _senador.find('PARLAPELLIDOMATERNO').text,
            'region': str(_senador.find('REGION').text).strip(),
            'circunscripcion': _senador.find('CIRCUNSCRIPCION').text,
            'partido': _senador.find('PARTIDO').text,
            'telefono': _senador.find('FONO').text,
            'email': _senador.find('EMAIL').text,
        }

        # Tratar nombres
        proto_nombres = str(_senador.find('PARLNOMBRE').text).strip()
        proto_nombres = proto_nombres.split(' ')

        senador['primer_nombre'] = proto_nombres[0]
        senador['segundo_nombre'] = ''
        if len(proto_nombres) > 1:
            senador['segundo_nombre'] = ' '.join(proto_nombres[1:])

        print(senador)
        lista_senadores.append(senador)

    return lista_senadores


if __name__ == '__main__':
    import json
    print('Scrappers Senado.cl - Project Snitch')
    print('Buscando senadores en senado.cl')
    lista = get_lista_senadores()

    print('Escribiendo a JSON')

    fecha = datetime.now()
    fecha_nombre = f'{fecha.year}-{fecha.month}-{fecha.day}'
    nombre_json = f'senadores-{fecha_nombre}.json'

    with open(f'../../datos/{nombre_json}', 'w') as f:
        json.dump(lista, f)

    print(f'Guardado en {nombre_json}')
    print('ok!')
