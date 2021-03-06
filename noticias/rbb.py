"""
    Spider biobiochile.cl
    Patricio Labin Correa - 2018
    GPLv3
"""
from datetime import datetime, timedelta
from time import sleep
from noticias.scrappers import ScrapperRBB
from noticias import db, Noticia, Legislador, FuenteNoticias
from noticias import logger
from application.app.my_tools.funciones import buscar_nombres_texto

NOMBRE = 'biobiochile.cl'
URL = 'http://www.biobiochile.cl/'
SCRIPT = 'rbb.py'


def obtener_fuente():
    fuente = FuenteNoticias.query.filter_by(nombre=NOMBRE).first()

    if not fuente:
        logger.warning('La fuente no existe. creando...')
        _fuente = FuenteNoticias(NOMBRE, URL, SCRIPT)
        db.session.add(_fuente)
        db.session.commit()
        fuente = _fuente
        logger.warning('ok')

    return fuente


def agregar_noticias():
    logger.info('Ejecutando Script.')
    fuente = obtener_fuente()
    scrapper = ScrapperRBB()
    lista_legisladores = Legislador.query.filter_by(buscar_noticias=True).all()

    # Obtener el dia anterior (de manera correcta).
    ahora = datetime.now()
    fecha = datetime(ahora.year, ahora.month, ahora.day) - timedelta(days=1)

    for intento in range(3):
        lista_a_noticias_dia = scrapper.get_lista_noticias_dia(fecha=fecha)
        if lista_a_noticias_dia:
            break
        else:
            sleep(15)

    noticias = []
    for a_noticia in lista_a_noticias_dia:
        _noticia = None

        for intento in range(3):
            link = a_noticia['link']
            if 'reportajes' in link:
                _noticia = scrapper.get_reportaje(link)
            elif '/noticias/deportes/' in link:
                _noticia = scrapper.get_deporte(link)
            else:
                _noticia = scrapper.get_regular(link)

            if _noticia:
                break

        if _noticia:
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
        print(f'{n.titulo} - {n.legisladores}')

    logger.info('Total Noticias Encontradas = ' + str(len(noticias)))

    db.session.remove()  # Reiniciar session
    for n in noticias:
        db.session.add(n)
    db.session.commit()

    logger.info('Fin Agregado')


if __name__ == '__main__':
    agregar_noticias()
