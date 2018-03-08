"""
    Scrapper Radio BioBio
    Patricio Labin Correa - 2018
    GPLv3
"""
import re
import traceback
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from project_snitch.noticias.scrappers import ScrapperNoticias
from project_snitch.noticias import logger


class ScrapperRBB(ScrapperNoticias):
    """
    Scrapper RBB.

    Attributes:
        url_template_paginacion: Lista que funciona como template para recorrer la seccion paginada.
                                    [0] = inicio del template
                                    <- Numero de la pagina ->
                                    [1] = fin del template
    """
    def __init__(self, url_template_paginacion=None):
        """
        Args:
            url_template_paginacion: Lista que funciona como template para recorrer la seccion paginada.
                                    [0] = inicio del template
                                    <- Numero de la pagina ->
                                    [1] = fin del template
        """
        if not url_template_paginacion:
            self.url_template_paginacion = ['http://www.biobiochile.cl/lista/nacional/categoria/chile?n=',
                                            '#/p?n=0&o=desc&r=all&cat=all&cont=no']
        else:
            self.url_template_paginacion = url_template_paginacion

    def get_noticia(self, url_pagina):
        if 'reportajes' in url_pagina:
            return self.get_reportaje(url_pagina)
        elif '/noticias/deportes/' in url_pagina:
            return self.get_deporte(url_pagina)
        else:  # Revisar contenido de la noticia
            page = requests.get(url_pagina)
            soup = BeautifulSoup(page.content, 'lxml')

            # Revisar Mujer
            try:
                href_mujer = soup.nav.ul.find_all('li')[1].a['href']
                if '/lista/mujer/' in href_mujer:
                    print('hola')
                    return self.get_mujer(url_pagina)
            except (AttributeError, IndexError) as err:
                pass

            # Obtener noticia normal
            return self.get_regular(url_pagina)

    def get_reportaje(self, url_pagina):
        """
        Obtiene un reportaje desde rbb.cl, se necesita una funcion completamente diferente porque se usa un layout distinto.
        Args:
            url_pagina (str): Url al reportaje

        Returns:
            dict: Reportaje
                    - titulo (str): Titulo del reportaje
                    - contenido (str): Texto plano extraido del reportaje
                    - link (str): URL al reportaje.
        """

        try:
            logger.info(f'Obteniendo reportaje desde: {url_pagina}')

            page = requests.get(url_pagina)

            soup = BeautifulSoup(page.content, 'lxml')

            reportaje = {'link': url_pagina}

            # Obtener Titulo
            scripts = soup.find_all('script')
            for i, _s in enumerate(scripts):
                if 'title_to_sanitize' in _s.text:
                    buscar_titulo = re.search("'.*'", _s.text)
                    titulo = buscar_titulo.group(0).replace('\'', '')
                    reportaje['titulo'] = titulo
            ##

            # Obtener Contenido
            extracto = 'EXTRACTO: ' + soup.find('p', {'id': 'extracto'}).text

            noticia_ps = soup.find('div', {'class': 'noticia-contenido'}).find_all('p')
            parrafos = []
            for _p in noticia_ps:
                _id = _p.get('id') or _p.get('class')
                if not _id:
                    if _p.text != '':
                        parrafos.append(_p.text)

            reportaje['contenido'] = '\n'.join((extracto, *parrafos))
            ##

        except Exception as exc:
            logger.error(traceback.format_exc())
            return None

        return reportaje

    def get_regular(self, url_pagina):
        """
        Obtiene una noticia regular desde rbb.cl.

        Args:
            url_pagina (str): Url de Noticia a obtener.

        Returns:
            dict: Noticia:
                    -  titulo (str): Titulo de la noticia.
                    - contenido (str): Contenido de la noticia.
                    - link (str): URL a la noticia.
        """
        try:
            logger.info(f'Obteniendo noticia desde: {url_pagina}')

            page = requests.get(url_pagina)

            soup = BeautifulSoup(page.content, 'lxml')

            noticia = {'link': url_pagina}

            # Titulo Noticia
            titulo = soup.find('h1', {'id': 'titulo-nota'}).text
            titulo = str(titulo).strip()
            noticia['titulo'] = titulo

            # Contenido Nota
            parrafos = soup.find('div',
                                 {"class": "contenido-nota"}).find_all('p')
            contenido = []
            for parrafo in parrafos:
                contenido.append(parrafo.text.strip())

            noticia['contenido'] = '\n'.join(contenido)

        except Exception:
            logger.error(traceback.format_exc())
            return None

        return noticia

    def get_deporte(self, url_pagina):
        """
        Obtiene una noticia de la seccion de deportes desde rbb.cl.

        Args:
            url_pagina (str): Url de Noticia a obtener.

        Returns:
            dict: Noticia:
                    - titulo (str): Titulo de la noticia.
                    - contenido (str): Contenido de la noticia.
                    - link (str): URL a la noticia.
        """
        try:
            logger.info(f'Obteniendo noticia desde: {url_pagina}')

            page = requests.get(url_pagina)

            soup = BeautifulSoup(page.content, 'lxml')

            noticia = {'link': url_pagina}

            # Titulo Noticia
            titulo = soup.find('h1', {'id': 'titulo-nota'}).text
            titulo = str(titulo).strip()
            noticia['titulo'] = titulo

            # Contenido Nota
            parrafos = soup.find('div',
                                 {"class": "box-post"}).find_all('p')
            contenido = []
            for parrafo in parrafos:
                contenido.append(parrafo.text.strip())

            noticia['contenido'] = '\n'.join(contenido)

        except Exception as exc:
            logger.error(traceback.format_exc())
            return None

        return noticia

    def get_mujer(self, url_pagina):
        """
        Obtiene una noticia desde la seccion mujer de rbb.cl.

        Args:
            url_pagina (str): Url de Noticia a obtener.

        Returns:
            dict: Noticia:
                    -  titulo (str): Titulo de la noticia.
                    - contenido (str): Contenido de la noticia.
                    - link (str): URL a la noticia.
        """
        try:
            logger.info(f'Obteniendo noticia desde: {url_pagina}')

            page = requests.get(url_pagina)

            soup = BeautifulSoup(page.content, 'lxml')

            noticia = {'link': url_pagina}

            # Titulo Noticia
            titulo = soup.find('h1', {'id': 'titulo_nota'}).text
            titulo = str(titulo).strip()
            noticia['titulo'] = titulo

            # Contenido Nota
            parrafos = soup.find('div',
                                 {"class": "parrafo"}).find_all('p')
            contenido = []
            for parrafo in parrafos:
                contenido.append(parrafo.text.strip())

            noticia['contenido'] = '\n'.join(contenido)

        except Exception:
            logger.error(traceback.format_exc())
            return None

        return noticia

    def get_lista_noticias_dia(
            self,
            url_nacional_paginacion=None,
            fecha=datetime.now()):
        """
        Obtiene la lista de noticias desde la seccion nacional de rbb en un determinado día.

        Args:
            url_nacional_paginacion (list): Lista que funciona como template para recorrer la seccion paginada.
                                            [0] = inicio del template
                                            <- Numero de la pagina ->
                                            [1] = fin del template
            fecha (datetime): Fecha de la que se extrae el dia y el mes para obtener las noticias

        Returns:
            lista_a_noticias (list): Lista de links a las noticias del dia.
        """
        mes, dia = fecha.month, fecha.day

        lista_a_noticias = []

        buscando = True
        iniciando = True
        pagina = 0
        print('Obteniendo Links a Noticias.')
        while buscando:
            if not url_nacional_paginacion:
                url_nacional_paginacion = self.url_template_paginacion
            url_pagina = f'{url_nacional_paginacion[0]}{pagina}{url_nacional_paginacion[1]}'
            logger.info(f'Pagina: {url_pagina}')
            page = requests.get(url_pagina)

            soup = BeautifulSoup(page.content, 'lxml')

            lista_noticias = soup.find('ul',
                                       {'id': 'results-list'}).find_all('li')

            for a_noticia in lista_noticias:
                _fecha = a_noticia.a.span.text
                noticia = {'link': a_noticia.a['href'],
                           'fecha': datetime.strptime(_fecha, '%d/%m/%Y %H:%M')}
                datetime_noticia = noticia['fecha']

                logger.info(noticia)

                if datetime_noticia.month == mes and datetime_noticia.day == dia:
                    lista_a_noticias.append(noticia)
                    iniciando = False
                else:
                    if not iniciando:
                        buscando = False
                        break
            pagina += 1

        logger.info('ok')
        return lista_a_noticias


if __name__ == '__main__':
    # Test Scrapping diario
    s = ScrapperRBB()

    noticias = []

    d = datetime(2018, 2, 7)

    for link_noticia in s.get_lista_noticias_dia(fecha=d):
        link = link_noticia['link']
        if 'reportajes' in link_noticia['link']:
            noticias.append(s.get_reportaje(link))
        else:
            noticias.append(s.get_regular(link))

    for _n in noticias:
        print(_n)