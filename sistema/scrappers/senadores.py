"""
    Scrapper Senadores
    Patricio Labin Correa (F1r3f0x) - 2017
    GPLv3
"""
import re
from bs4 import BeautifulSoup
from requests import get as requests_get
from requests import exceptions as requests_exceptions


URL_LISTADO_SENADORES = 'http://www.senado.cl/appsenado/index.php?mo=senadores&ac=listado'


def get_datos_perfil(url_senador):
    """
    Obtiene Telefono, Email y distritos de un Senador desde su perfil
    :param url_senador:
    :type url_senador:
    :return: datos
    :rtype: dict
    """
    try:
        page = requests_get(url_senador)
    except (ConnectionError, ConnectionRefusedError, requests_exceptions.MissingSchema) as err:
        print(f'Error al obtener datos del perfil: {url_senador}')
        print(err)
        return None

    soup = BeautifulSoup(page.content, 'lxml')

    info = {}

    # Mail / telefono
    try:
        div_mail_telefono = soup.find('div', {'class': 'datos'})
    except AttributeError as err:
        print(f'Error al iniciar Scrapping del perfil: {url_senador}')
        print(err)
        return None

    lis_datos = div_mail_telefono.find_all('li')

    for n_li, item in enumerate(lis_datos):
        hijos = item.children
        texto = ''
        for n_hijo, hijo in enumerate(hijos):
            if n_hijo == 1:
                texto = str(hijo).strip()

        if item.find('strong'):
            if item.find('strong').text == 'Teléfono:':
                info['telefono'] = texto
            if item.find('strong').text == 'Mail:':
                info['email'] = texto

    # Distritos
    li_distritos = soup.find('div', {'class': 'col2 aright'}).ul.find_all('li')[3].children

    for n_child, child in enumerate(li_distritos):
        if n_child == 1:
            distritos_raw = str(child).replace('y', ',')
            distritos_raw = distritos_raw.split(',')
            distritos = []
            for dis in distritos_raw:
                distritos.append(dis.strip())

            info['distritos'] = distritos

    return info


def get_lista_senadores():
    """
    Obtiene la lista de senadores con sus datos desde la pagina del Senado.
    :return: lista_senadores
    :rtype: dict
    """
    try:
        print('Obteniendo Lista')
        page = requests_get(URL_LISTADO_SENADORES)
    except (ConnectionError, ConnectionRefusedError, requests_exceptions.MissingSchema) as err:
        print(f'Error al obtener listado del Senado: {err}')
        return None

    soup = BeautifulSoup(page.content, 'lxml')

    try:
        print('Iniciando Scrapping')
        # Nombres legisladores
        td_senadores = soup.find_all('td', {'style': 'width: 85%;'})
        num_sen = 0

        # Partidos Senadores
        tr_partidos = soup.find_all('tr', {'align': 'left'})
    except AttributeError as err:
        print(f'Error al iniciar Scrapping en lista de Senadores: {err}')
        return None

    senadores = []
    cont_partido = 1
    print('Obteniendo Senadores')
    for td_senador in td_senadores:
        # Obteners tds por div
        divs_senador = td_senador.find_all('div')
        for i, div_senador in enumerate(divs_senador):
            if i == 0:  # Nombre
                nuevo_senador = {}
                nuevo_senador['tipo'] = 'Senador'

                # Nombre - Primer div es el nombre
                nombre = div_senador.text
                nombre = str(nombre).split(',')  # SP PP, PN SN
                apellidos = nombre[0].split(' ')

                # Obtener apellidos de multiples palabras (gente subnormal)
                if len(apellidos) > 2:  # FUCK NAMES
                    largo = len(apellidos)
                    primer_apellido = ''
                    for a in range(largo-1):
                        primer_apellido += '{} '.format(apellidos[a])
                    nuevo_senador['primer_apellido'] = primer_apellido.rstrip()
                    nuevo_senador['segundo_apellido'] = apellidos[largo-1]

                # Apellidos de gente nomrmal!
                else:
                    nuevo_senador['primer_apellido'] = apellidos[0]
                    nuevo_senador['segundo_apellido'] = apellidos[1]

                # Nombre
                nombres = nombre[1].strip().split(' ')
                nuevo_senador['primer_nombre'] = nombres[0]
                if len(nombres) > 1:
                    nuevo_senador['segundo_nombre'] = nombres[1]
                else:
                    nuevo_senador['segundo_nombre'] = ' '

                # Partido
                nuevo_senador['partido'] = tr_partidos[cont_partido].td.next_sibling.next_sibling.strong.text.strip()
                cont_partido += 1

                # Link
                link_senador = div_senador.a['href']
                link = 'http://www.senado.cl/{}'.format(link_senador)
                nuevo_senador['link'] = link

                # Email / Telefono / Distritos
                datos_perfil = get_datos_perfil(link)
                if datos_perfil:
                    nuevo_senador['telefono'] = datos_perfil['telefono']
                    nuevo_senador['email'] = datos_perfil['email']
                    nuevo_senador['distritos'] = datos_perfil['distritos']

                # Id
                id_interna = re.search('\d.+', link_senador)
                nuevo_senador['id_interna'] = id_interna.group(0)
            elif i == 1:  # 1° <strong> region, 2° <strong> circunscripcion
                strong_region = div_senador.find('strong')
                nuevo_senador['region'] = str(strong_region.text).strip()
                nuevo_senador['circunscripcion'] = strong_region.next_sibling.next_sibling.text
                num_sen += 1
            else:
                break

        print(f'Senador Agregado [{nuevo_senador["id_interna"]}]: {nuevo_senador["primer_nombre"]} {nuevo_senador["primer_apellido"]} - {nuevo_senador["partido"]}')
        senadores.append(nuevo_senador)

    print('Lista terminada')
    print(f'Senadores Obtenidos: {len(senadores)}')
    return senadores


if __name__ == '__main__':
    import json
    lista = get_lista_senadores()

    print('Escribiendo a JSON')
    with open('../datos/senadores.json', 'w') as f:
        json.dump(lista, f)
