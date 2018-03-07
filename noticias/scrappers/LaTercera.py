"""
    Scrapper La Tercera
    Patricio Labin Correa - 2018
    GPLv3
"""
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from project_snitch.noticias.scrappers import ScrapperNoticias
from project_snitch.noticias import logger


class ScrapperLaTercera (ScrapperNoticias):

    def __init__(self, url_nacional=None, url_politica=None):
        if not url_nacional:
            self.url_nacional = 'http://www.latercera.com/nacional/page/'
        else:
            self.url_nacional = url_nacional

        if not url_politica:
            self.url_politica = 'http://www.latercera.com/politica/page/'
        else:
            self.url_politica = url_politica

    def get_noticia(self, url_pagina: str):
        """
        Obtiene una noticia regular desde latercera.com.

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
            titulo = soup.find('h1', {'class': 'm-top-30'}).text
            titulo = str(titulo).strip()
            noticia['titulo'] = titulo

            contenido = []

            # Bajada
            bajada = soup.find('div', {'class': 'bg-gray bajada-art'})
            if bajada:
                bajada = bajada.h2.text
                contenido.append(bajada)

            # Contenido Nota
            primer_elemento = soup.find('div', {"id": "ambideXtro"}).contents[0]

            for elemento in primer_elemento.find_next_siblings():
                if elemento != '\n' and elemento.name in ['h1', 'h2', 'p']:
                    contenido.append(elemento.text)

            noticia['contenido'] = '\n'.join(contenido)

            return noticia
        except Exception as exc:
            logger.error(exc)
            return None

    def get_lista_noticias_dia(self,
                               url_nacional=None,
                               url_politica=None,
                               fecha=datetime.now()):
        """
        Obtiene la lista de noticias desde las secciones de politica y nacional de latercera.com

        Args:
            url_politica (str): URL a seccion de Politica.
            url_nacional (str): URL a seccion Nacional.
            fecha (datetime): Fecha de la que se extrae el dia y el mes para obtener las noticias.

        Returns:
            lista_a_noticias (list): Lista de links a las noticias del dia.
        """
        if not url_nacional:
            url_nacional = self.url_nacional
        if not url_politica:
            url_politica = self.url_politica

        mes, dia = fecha.month, fecha.day

        lista_a_noticias = []

        secciones = [url_nacional, url_politica]

        logger.info(f'Obteniendo Links a Noticias para dia {fecha}')
        for seccion in secciones:
            buscando = True
            iniciando = True
            pagina = 1
            while buscando:
                url_pagina = seccion + str(pagina)
                logger.info(f'Pagina: {url_pagina}')
                page = requests.get(url_pagina)

                soup = BeautifulSoup(page.content, 'lxml')

                lista_noticias = soup.find_all('article', {'class': 'border-bottom-1 archive-article'})

                for a_noticia in lista_noticias:
                    _fecha = a_noticia.find('small', {'class': 'time-ago'}).text.strip()
                    noticia = {'link': a_noticia.a['href'],
                               'fecha': datetime.strptime(_fecha, '%d/%m/%Y %I:%M %p')}
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
    s = ScrapperLaTercera()

    d = datetime(2018, 2, 8)
    print(s.get_lista_noticias_dia(fecha=d))