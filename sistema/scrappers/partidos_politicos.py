"""
    Scrapper Partidos Politicos
    Patricio Labin Correa (F1r3f0x) - 2017
    GPLv3
"""
import json
import requests
from bs4 import BeautifulSoup

URL_WIKI_LISTA_PP = 'https://es.wikipedia.org/wiki/Partidos_pol%C3%ADticos_de_Chile'


# TODO: obtener logo
def get_partidos_politicos(url_pagina):
    """
    Obtiene una lista de los partidos politicos de chile desde wikipedia
    :param url_pagina:
    :type url_pagina:
    :return:
    :rtype:
    """
    try:
        page = requests.get(url_pagina)

        soup = BeautifulSoup(page.content, 'lxml')

        tabla = soup.find('table', attrs={'class': 'wikitable'})
        filas_tabla = tabla.find_all('tr')

        lista_partidos = []
        id_partido = 1
        for i, fila in enumerate(filas_tabla):
            if i > 0:
                nombre = fila.td.a.text
                datos_fila = fila.find_all('td')
                estado = datos_fila[1].text
                if estado == 'Constituido':
                    lista_partidos.append({'id': id_partido, 'nombre': nombre})
                    id_partido += 1

        return lista_partidos

    except:
        return None


if __name__ == '__main__':
    partidos = get_partidos_politicos(URL_WIKI_LISTA_PP)
    print(partidos)
