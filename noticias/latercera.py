"""
    Spider La Tercera
    Patricio Labin Correa - 2018
    GPLv3
"""
from datetime import datetime, timedelta
from time import sleep
from sqlalchemy.exc import OperationalError
from project_snitch.noticias.scrappers import ScrapperLaTercera
from project_snitch.noticias import db, Noticia, Legislador, FuenteNoticias
from project_snitch.noticias import logger
from project_snitch.my_tools.funciones import buscar_nombres_texto

NOMBRE = 'La Tercera'
URL = 'http://www.latercera.com/'
SCRIPT = 'latercera.py'


def obtener_fuente():
    try:
        fuente = FuenteNoticias.query.filter_by(nombre=NOMBRE).first()

        if not fuente:
            logger.warning('La fuente no existe. creando...')
            _fuente = FuenteNoticias(NOMBRE, URL, SCRIPT)
            db.session.add(_fuente)
            db.session.commit()
            fuente = _fuente
            logger.warning('ok')

        return fuente
    except OperationalError as err:
        logger.error(err)
        return None


def agregar_noticias():
    logger.info('Ejecutando Script.')

    fuente = obtener_fuente()
    scrapper = ScrapperLaTercera()
    lista_legisladores = Legislador.query.filter_by(buscar_noticias=True).all()

    # Obtener el dia anterior (de manera correcta).
    ahora = datetime.now()
    fecha = datetime(ahora.year, ahora.month, ahora.day) - timedelta(days=1)

    while True:
        lista_a_noticias_dia = scrapper.get_lista_noticias_dia(fecha=fecha)
        if lista_a_noticias_dia:
            break
        else:
            sleep(15)

    noticias = []
    for a_noticia in lista_a_noticias_dia:
        while True:
            _noticia = scrapper.get_noticia(a_noticia['link'])

            if _noticia:
                break

        noticia = Noticia(_noticia['titulo'],
                          _noticia['link'],
                          contenido_texto=_noticia['contenido'],
                          fecha=a_noticia['fecha'],
                          )
        noticia.fuente = fuente

        legisladores_encontrados = []
        for legislador in lista_legisladores:
            if buscar_nombres_texto(noticia.contenido_texto,
                                    legislador.primer_nombre,
                                    legislador.segundo_nombre,
                                    legislador.primer_apellido,
                                    legislador.segundo_apellido):
                legisladores_encontrados.append(legislador)

        if len(legisladores_encontrados) > 0:
            noticia.legisladores = legisladores_encontrados
            noticias.append(noticia)

    logger.info('Noticias con Legisladores Encontradas:')
    for n in noticias:
        logger.info(f'{n.titulo} - {n.legisladores}')

    logger.info('Total Noticias Encontradas = ' + str(len(noticias)))

    db.session.remove()  # Reiniciar session
    for n in noticias:
        db.session.add(n)
    db.session.commit()

    logger.info('Fin agregado.')


if __name__ == '__main__':
    agregar_noticias()