"""
    Scrappers de sitios de noticias.
    Patricio Labin Correa (F1r3f0x) - 2017
    GPLv3
"""
import json
import requests
from bs4 import BeautifulSoup


def get_noticia_latercera(url_pagina):
    try:
        page = requests.get(url_pagina)

        soup = BeautifulSoup(page.content, 'lxml')

        noticia = {}

        titulo = soup.find('h1', attrs={'class': 'titulo_ficha'}).text
        noticia['titulo'] = titulo

        contenido = soup.find('div', attrs={'class': 'contenido'}).text
        noticia['contenido'] = contenido

        return noticia

    except:
        return None


def get_noticia_emol(url_pagina):
    try:
        page = requests.get(url_pagina)

        soup = BeautifulSoup(page.content, 'lxml')

        noticia = {}

        # Titulo Noticia
        titulo = soup.find('h1', {'id': 'cuDetalle_cuTitular_tituloNoticia'}).text
        titulo = str(titulo).strip()
        noticia['titulo'] = titulo

        # Contenido Noticia
        divs_contenido = soup.find('div', attrs={'id': 'cuDetalle_cuTexto_textoNoticia'})
        contenido = ''
        for i, div_contenido in enumerate(divs_contenido):
            if not div_contenido.find('br'):
                if i == 0:
                    contenido = '{}'.format(div_contenido.text)
                if i > 0:
                    contenido = '{}\n{}'.format(contenido, div_contenido.text)

        print(contenido)
        noticia['contenido'] = contenido
        
        return noticia

    except:
        return None
