"""
    Mantenedor Legisladores
    Patricio Labin Correa (F1r3f0x) - 2017-2018
    GPLv3
"""
import json
import pymysql.cursors
from sistema.scrappers.senadores import get_lista_senadores
from sistema.scrappers.diputados import get_lista_diputados
from project_snitch.my_tools.funciones import get_texto_buscable

# DB Variables
DB_HOST = 'example.net'
DB_PORT = 3306
DB_USER = 'user'  # Credenciales Aqui!!!
DB_PASS = 'pass'  # Y Aqui
DB_NAME = 'Snitch'
DB_CHARSET = 'utf8mb4'

# Variables
ID_TIPO_SENADOR = 1
ID_TIPO_DIPUTADO = 2
ID_PERIODO = 9


# Traduccion de datos
# Senadores
TRADUCCION_REGIONES_SENADORES = {
    'Región de Tarapacá':                                   2,
    'Región de Antofagasta':                                3,
    'Región de Atacama':                                    4,
    'Región de Coquimbo':                                   5,
    'Región de Valparaíso':                                 6,
    'Región Metropolitana':                                 7,
    'Región del Libertador General Bernardo O\'Higgins':    8,
    'Región del Maule':                                     9,
    'Región del Bío-Bío':                                   10,
    'Región de la Araucanía':                               11,
    'Región de los Ríos':                                   12,
    'Región de Los Lagos':                                  13,
    'Región de Aysén del General Carlos Ibáñez del Campo':  14,
    'Región de Magallanes y la Antártica Chilena':          15
}

TRADUCCION_PARTIDOS_SENADORES = {
    'U.D.I.':           1,
    'R.N.':             2,
    'P.S.':             3,
    'P.D.C.':           4,
    'P.P.D.':           5,
    'PAÍS':             10,
    'Amplitud':         20,
    'Independiente':    9999
}
# Diputados
TRADUCCION_REGIONES_DIPUTADOS = {
    'XV Región Arica y Parinacota':                             1,
    'I Región de Tarapacá':                                     2,
    'II Región de Antofagasta':                                 3,
    'III Región de Atacama':                                    4,
    'IV Región de Coquimbo':                                    5,
    'V Región de Valparaíso':                                   6,
    'RM Región Metropolitana':                                  7,
    'VI Región del Libertador Bernardo O\' Higgins':            8,
    'VII Región del Maule':                                     9,
    'VIII Región del Bío Bío':                                  10,
    'IX Región de la Araucanía':                                11,
    'XIV Región de los Ríos':                                   12,
    'X Región de los Lagos':                                    13,
    'XI Región de Aysén del General Carlos Ibáñez del Campo':   14,
    'XII Región de Magallanes y de la Antártica Chilena':       15
}

TRADUCCION_PARTIDOS_DIPUTADOS = {
    'Unión Demócrata Independiente':        1,
    'Renovación Nacional':                  2,
    'Partido Socialista':                   3,
    'Partido Demócrata Cristiano':          4,
    'Partido Por la Democracia':            5,
    'Evópoli':                              6,
    'Revolución Democrática':               7,
    'Partido Radical Social Demócrata':     8,
    'Partido Comunista':                    11,
    'Partido Liberal de Chile':             14,
    'Amplitud':                             20,
    'Izquierda Ciudadana':                  22,
    'Independientes':                       9999
}


# TODO: get_distrito_id
def get_distrito_id(numero_distrito):
    pass


# TODO: get_circun_id
def get_circun_id(numero_circuns, legislatura_antigua):
    if legislatura_antigua:
        return int(numero_circuns)
    else:
        # TODO
        return 0


def ingresar_legisladores(conn, cur, list_legisladores, id_periodo):
    """
    Ingreso de primera vez de legisladores

    Args:
        conn (Connection): Conexion a DB.
        cur (Cursor): Cursor de conector a DB.
        list_legisladores (list): Diccionario con datos de los legisladores (obtenidos con su scrapper)
        id_periodo (int): El periodo legislativo de los legisladores.

    Returns:
        bool: Resultado de la operacion.

    """

    if list_legisladores:
        # Ingresar Legislador
        query = 'INSERT INTO legislador (primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, email, telefono, texto_buscable, activo) VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE )'
        cnt_id = 0
        for legislador in list_legisladores:
            print(f'Legislador: {legislador["primer_nombre"]} {legislador["primer_apellido"]}')

            texto_no_buscable = f"{legislador['primer_nombre']} {legislador['segundo_nombre']} {legislador['primer_apellido']} {legislador['segundo_apellido']}"
            texto_buscable = get_texto_buscable(texto_no_buscable)

            cur.execute(query,
                           (legislador['primer_nombre'],
                            legislador['segundo_nombre'],
                            legislador['primer_apellido'],
                            legislador['segundo_apellido'],
                            legislador['email'],
                            legislador['telefono'],
                            texto_buscable)
                           )

            cnt_id += 1
            legislador['id'] = cnt_id

        conn.commit()

        # Ingresar cargo
        cargo_id = 0
        for legislador in list_legisladores:
            if legislador['tipo'] == ID_TIPO_SENADOR:
                query = f'INSERT INTO snitch.cargo_legislativo (legislador_id, remuneracion, tipo_legislador_id, partido_politico_id, periodo_id, region_id, circunscripcion_id, id_interna, activo) VALUES (%s, 0, %s, %s, {id_periodo}, %s, %s, %s, TRUE)'
            else:
                query = f'INSERT INTO snitch.cargo_legislativo (legislador_id, remuneracion, tipo_legislador_id, partido_politico_id, periodo_id, region_id, id_interna, activo) VALUES (%s, 0, %s, %s, {id_periodo}, %s, %s, TRUE)'

            print(f'Cargo Legislativo: [{legislador["tipo"]}] {legislador["primer_nombre"]} {legislador["primer_apellido"]} id: {legislador["id"]}')
            if legislador['tipo'] == ID_TIPO_SENADOR:
                cur.execute(query,
                               (legislador['id'],
                                legislador['tipo'],
                                legislador['partido'],
                                legislador['region'],
                                legislador['circunscripcion'],
                                legislador['id_interna'])
                               )
            else:
                cur.execute(query,
                            (legislador['id'],
                             legislador['tipo'],
                             legislador['partido'],
                             legislador['region'],
                             legislador['id_interna'])
                            )
            cargo_id +=1
            legislador['cargo_id'] = cargo_id
        conn.commit()

        # Ingresar distritos
        query = 'INSERT INTO snitch.distrito_cargo_legislativo VALUES (%s, %s)'
        for legislador in list_legisladores:
            print(f'Distritos: {legislador["primer_nombre"]} {legislador["primer_apellido"]}')
            if legislador['tipo'] == ID_TIPO_SENADOR:
                for distrito in legislador['distritos']:
                    cur.execute(query,
                                (distrito,
                                 legislador['cargo_id']))
            else:
                cur.execute(query,
                            (legislador['distrito'], legislador['cargo_id']))
        conn.commit()
        return True
    else:
        return False


def get_actualizar_senadores(conn, cur, dict_senadores_actualizar, dict_senadores_nuevos=None):
    """
    Actualizacion e Ingreso de nuevos senadores
    :param conn:
    :type conn:
    :param cur:
    :type cur:
    :param dict_senadores_actualizar:
    :type dict_senadores_actualizar:
    :param dict_senadores_nuevos:
    :type dict_senadores_nuevos:
    :return:
    :rtype:
    """
    pass


if __name__ == '__main__':

    conn = None
    try:
        conn = pymysql.connect(host=DB_HOST,
                               port=DB_PORT,
                               user=DB_USER,
                               db=DB_NAME,
                               password=DB_PASS,
                               charset=DB_CHARSET,
                               cursorclass=pymysql.cursors.DictCursor)
    except Exception as err:
        print(f'Error al conectar a la DB: {err}')
        quit()

    print("\nMantenedor Project Snitch\n")

    # Variables de Control
    periodo_id = 0  # Periodo de los legisladores
    legislatura_antigua = False  # Legislatura de los legisladores (por el cambio de distritos)
    lista_legisladores = []

    dir_archivo_diputados = '../datos/diputados.json'
    dir_archivo_senadores = '../datos/senadores.json'

    lista_senadores = []
    lista_diputados = []

    # Obtener Periodos
    periodos = []
    query = 'SELECT * FROM snitch.periodo ORDER BY id'
    with conn.cursor() as _cursor:
        _cursor.execute(query)
        periodos = _cursor.fetchall()

    # Obtener ids de periodos
    ids_periodos = [p['id'] for p in periodos]

    # Imprimir lista de periodos
    print('Seleccione Periodo Legislativo de Legisladores: \n')
    for p in periodos:
        print(f'{p["id"]}._ {p["nombre"]} ({p["año_inicio"]}-{p["año_fin"]})')

    # Seleccionar un periodo para el ingreso
    obteniendo = True
    while obteniendo:
        try:
            periodo_id = int(input('\nNumero de periodo a ingresar: '))
        except ValueError as err:
            print('Ingrese un numero!')
            continue
        if periodo_id in ids_periodos:
            obteniendo = False
        else:
            print('El periodo no existe, intente de nuevo.')

    if periodo_id <= 9:
        legislatura_antigua = True

    print(f'Legislatura Antigua = {legislatura_antigua}')

    # Desde archivo o web
    while True:
        fuente = str(input('Desde (A)rchivos o (W)eb?')).lower().strip()

        if fuente == 'a':
            print('Cargando desde archivo')
            with open(dir_archivo_diputados, 'r', encoding='utf8') as _file:
                lista_diputados = json.load(_file)
            with open(dir_archivo_senadores, 'r', encoding='utf8') as _file:
                lista_senadores = json.load(_file)
            print('Cargados')
            break

        if fuente == 'w':
            print('Obteniendo Legisladores')
            print('Diputados:')
            lista_diputados = get_lista_diputados()
            print('Senadores:')
            lista_senadores = get_lista_senadores()
            break

    print('Creando Lista Maestra')
    lista_legisladores.extend(lista_diputados)
    lista_legisladores.extend(lista_senadores)

    print(f'Legisladores Obtenidos: {len(lista_legisladores)}')

    # Traducir datos
    for legislador in lista_legisladores:
        region = legislador['region']
        partido = legislador['partido']
        if legislador['tipo'] == 'Senador':
            legislador['tipo'] = 1
            legislador['region'] = TRADUCCION_REGIONES_SENADORES.get(region)
            legislador['partido'] = TRADUCCION_PARTIDOS_SENADORES.get(partido)
        else:
            legislador['tipo'] = 2
            legislador['region'] = TRADUCCION_REGIONES_DIPUTADOS.get(region)
            legislador['partido'] = TRADUCCION_PARTIDOS_DIPUTADOS.get(partido)

    # Ingresar legisladores al sistema
    with conn.cursor() as cursor:
        resultado = ingresar_legisladores(conn, cursor, lista_legisladores, periodo_id)
        print(resultado)

else:
    print('THIS IS NOT A MODULE')
    quit(0)
