"""
    Funciones Varias
    Patricio Labin Correa - 2017
    GPLv3
"""
import json


def get_texto_buscable(texto: str):
    """
    Obtiene un texto buscable para Whoosh

    Args:
        texto (str): Texto a transformar

    Returns:
        str: Texto buscable de texto.
    """
    tildes = [
        {'tilde': 'á', 'reemplazo': 'a'},
        {'tilde': 'é', 'reemplazo': 'e'},
        {'tilde': 'í', 'reemplazo': 'i'},
        {'tilde': 'ó', 'reemplazo': 'o'},
        {'tilde': 'ú', 'reemplazo': 'u'},
    ]

    nuevo_texto = texto.lower()

    for letra in tildes:
        nuevo_texto = nuevo_texto.replace(letra['tilde'], letra['reemplazo'])

    return nuevo_texto


def get_diferencias_lista_senadores():
    """
    Obtiene diferencias entre sets de senadores
    TODO
    :return:
    :rtype:
    """
    dict_viejo = None
    with open('datos/senadores.json') as f:
        dict_viejo = json.load(f)
    dict_nuevo = None
    with open('datos/nuevos_senadores.json') as f:
        dict_nuevo = json.load(f)

    dict_nuevo['100'] = {'primer_nombre': 'perro', 'primer_apellido': 'perro', 'segundo_apellido': 'perro'}

    distintos = []

    print(dict_viejo.values())

    for senador_nuevo in dict_nuevo.values():
        existe = False
        for senador_viejo in dict_viejo.values():
            if senador_nuevo['primer_nombre'] and senador_nuevo['primer_apellido'] and senador_nuevo['segundo_apellido'] in senador_viejo.values():
                existe = True
                print(senador_nuevo)
        if not existe:
            distintos.append(senador_nuevo)
    return distintos


def buscar_nombres_texto(texto_a_buscar: str, primer_nombre='', segundo_nombre=None, primer_apellido='', segundo_apellido=None):
    """
    Busca una persona en un texto. Usada para buscar legisladores en noticias.

    Args:
        texto_a_buscar (str): El texto en el que se busca el nombre.
        primer_nombre (str):
        segundo_nombre (str):
        primer_apellido (str):
        segundo_apellido (str):

    Returns:
        bool: Si encuentra a la persona True
    """
    nombres_a_buscar = [
        ' '.join([primer_nombre, primer_apellido]),
        f'{primer_nombre[0]}. {primer_apellido}',
        f'{primer_nombre} {primer_apellido[0]}.',
    ]

    if segundo_apellido:
        nombres_a_buscar.append(' '.join([primer_nombre, primer_apellido, segundo_apellido]))

    if segundo_nombre and segundo_apellido:
        nombres_a_buscar.append(' '.join([primer_nombre, segundo_nombre, primer_apellido, segundo_apellido]))

    encontrar = False
    for nombre in nombres_a_buscar:
        if nombre in texto_a_buscar:
            encontrar = True

    return encontrar


def get_changelog(file_dir):
    parrafos = []
    with open(file_dir) as _f:
        for linea in _f:
            parrafos.append(linea.rstrip())
    return parrafos
