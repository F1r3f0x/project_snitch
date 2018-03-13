"""
    Scrapper Senadores
    Patricio Labin Correa (F1r3f0x) - 2018
    GPLv3
"""
import re
from datetime import datetime
from bs4 import BeautifulSoup
from requests import get as requests_get
from requests import exceptions as requests_exceptions

URL_DIPUTADOS_PERIODO_ACTUAL = "http://opendata.camara.cl/camaradiputados/WServices/WSDiputado.asmx/retornarDiputadosPeriodoActual"

URL_PERFIL_DIPUTADO = "https://www.camara.cl/camara/diputado_detalle.aspx?prmid="


def get_datos_perfil(url_perfil):
    try:
        req = requests_get(url_perfil)
    except (ConnectionError, ConnectionRefusedError,
            requests_exceptions.MissingSchema) as err:
        print(f'Error al obtener datos del perfil: {url_perfil}')
        print(err)
        return None

    soup = BeautifulSoup(req.content, 'lxml')

    try:
        ficha = soup.find('div', {'id': 'ficha'})
        ficha = ficha.find_all('div', {'class': 'col'})
    except AttributeError as err:
        print(f'Error al hacer scrapping de los datos del perfil: {url_perfil}')
        print(err)
        print('Ignorando datos de perfil')
        return None

    # 1 -> [div] imagen, fecha nacimiento
    # 2 -> [div] distrito, region
    # 3 -> [div] telefono, mail

    region = str(ficha[1].div.find_all('p')[2].a.text)  # [p]s con region
    region = region.replace('\n', '').replace('\r', '').strip()

    # Recorrer string region y eliminar espacios del centtro
    primera_string = ''
    pos_siguiente = 0
    for i, c in enumerate(region):
        if c != ' ':
            primera_string += c
        else:
            pos_siguiente = i
            break
    region = f'{primera_string} {region[pos_siguiente:].strip()}'

    email = soup.find('li', {'class': 'email'}).text.strip().\
        replace('\n', '').replace('\r', '')

    telefono = soup.find('div', {'class': 'phones'}).p.contents[2]
    telefono = re.findall('([1-9+()]+)', telefono)
    telefono = ''.join(telefono)

    return {'region': region,
            'email': email,
            'telefono': telefono}


def get_lista_diputados(_dev=False):
    """
    Obtiene la lista de los diputados desde el servicio web de la camara de diputados
    :param _dev: Flag modo desarrollo
    :type _dev: bool
    :return: Lista de diputados
    :rtype: dict
    """
    if not _dev:
        print('Obteniendo lista de Diputados desde URL')
        try:
            page = requests_get(URL_DIPUTADOS_PERIODO_ACTUAL)
        except (ConnectionError, ConnectionRefusedError,
                requests_exceptions.MissingSchema) as err:
            print(f'Error al obtener lista de diputados: {err}')
            return None

        soup = BeautifulSoup(page.content, 'xml')
    else:
        print('Obteniendo lista de Diputados desde archivo')
        soup = BeautifulSoup(_get_xml_dev(), 'xml')

    try:
        diputados_periodo = soup.find_all('DiputadoPeriodo')
    except AttributeError as err:
        print(
            'Error al obtener XML de diputados (no parece ser el archivo correcto)'
        )
        print(err)
        return None

    print('Agregando diputados a lista...')
    lista_diputados = []
    for diputado in diputados_periodo:
        nuevo_diputado = {}
        nuevo_diputado['tipo'] = 'Diputado'
        nuevo_diputado['primer_nombre'] = diputado.Diputado.Nombre.text
        nuevo_diputado['segundo_nombre'] = diputado.Diputado.Nombre2.text
        nuevo_diputado['primer_apellido'] = diputado.Diputado.ApellidoPaterno.text
        nuevo_diputado['segundo_apellido'] = diputado.Diputado.ApellidoMaterno.text
        nuevo_diputado['id_interna'] = diputado.Diputado.Id.text
        nuevo_diputado['distrito'] = diputado.Distrito.Numero.text
        nuevo_diputado['link'] = f'{URL_PERFIL_DIPUTADO}{nuevo_diputado["id_interna"]}'

        # Obtener Partido
        militancias = diputado.Diputado.Militancias.find_all("Militancia")
        ultima_militancia = militancias[-1]
        nuevo_diputado['partido'] = ultima_militancia.Partido.Nombre.text

        datos = get_datos_perfil(nuevo_diputado['link'])

        if datos:
            nuevo_diputado['region'] = datos['region']
            nuevo_diputado['email'] = datos['email']
            nuevo_diputado['telefono'] = datos['telefono']
        else:
            nuevo_diputado['region'] = ''
            nuevo_diputado['email'] = ''
            nuevo_diputado['telefono'] = ''

        print(nuevo_diputado)
        lista_diputados.append(nuevo_diputado)

    print(f'Diputados Obtenidos: {len(lista_diputados)}')
    return lista_diputados


def _get_xml_dev():
    with open('datos_prueba/diputadosPeriodoActual.xml', 'r', encoding='utf8') as _file:
        return _file.read()


if __name__ == "__main__":
    import json

    print('Scrapper Diputados - Project Snitch')

    diputados = get_lista_diputados()

    fecha = datetime.now()
    fecha_nombre = f'{fecha.year}-{fecha.month}-{fecha.day}'
    nombre_json = f'diputados-{fecha_nombre}.json'

    print('Escribiendo archivo JSON')
    if diputados:
        with open(f'../../datos/{nombre_json}', 'w', encoding='utf8') as _file:
            json.dump(diputados, _file)

    print(f'Guardado en {nombre_json}')
    print('ok!')
