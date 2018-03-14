"""
    Mantenedor Legisladores
    Patricio Labin Correa (F1r3f0x) - 2017-2018
    GPLv3
"""
import json
from datetime import datetime
from sqlalchemy import exc
from project_snitch.sistema.scrappers.senadores import get_lista_senadores
from project_snitch.sistema.scrappers.diputados import get_lista_diputados
from project_snitch import models, db

# Variables
ID_TIPO_SENADOR = 1
ID_TIPO_DIPUTADO = 2
LEGISLATURA_ANTIGUA = False

DIR_JSON_DIPUTADOS = 'datos/diputados.json'
DIR_JSON_SENADORES = 'datos/senadores.json'


# Traduccion de datos
# Senadores
TRADUCCION_REGIONES_SENADORES = {
    'Región de Arica y Parinacota':                         1,
    'Región de Tarapacá':                                   2,
    'Región de Antofagasta':                                3,
    'Región de Atacama':                                    4,
    'Región de Coquimbo':                                   5,
    'Región de Valparaíso':                                 6,
    'Región Metropolitana':                                 7,
    'Región Metropolitana de Santiago':                     7,
    'Región del Libertador General Bernardo O\'Higgins':    8,
    'Región del Maule':                                     9,
    'Región del Bío-Bío':                                   10,
    'Región de la Araucanía':                               11,
    'Región de los Ríos':                                   12,
    'Región de Los Ríos':                                   12,
    'Región de Los Lagos':                                  13,
    'Región de Aysén del General Carlos Ibáñez del Campo':  14,
    'Región de Magallanes y la Antártica Chilena':          15
}

TRADUCCION_PARTIDOS_SENADORES = {
    'U.D.I.':                       1,
    'R.N.':                         2,
    'P.S.':                         3,
    'P.D.C.':                       4,
    'P.P.D.':                       5,
    'Evopoli':                      6,
    'Revolución Democrática':       7,
    'PAÍS':                         10,
    'Amplitud':                     20,
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


def ingresar_legisladores(db, list_legisladores, id_periodo):
    """
    Ingreso de primera vez de legisladores

    Args:
        db (SQLAlchemy): ORM
        list_legisladores (list): Diccionario con datos de los legisladores (obtenidos con su scrapper)
        id_periodo (int): El periodo legislativo de los legisladores.

    Returns:
        bool: Resultado de la operacion.

    """
    legisladores_agregar = []

    for legislador in list_legisladores:
        # Legislador
        _legislador = models.Legislador(
            legislador['primer_nombre'],
            '',
            legislador['primer_apellido'],
            '',
            None,
            legislador['email'],
            legislador['telefono'],
            '',
            True,
            estado_noticioso_id=1,
        )
        segundo_nombre = legislador['segundo_nombre']
        if segundo_nombre:
            _legislador.segundo_nombre = segundo_nombre
        segundo_apellido = legislador['segundo_apellido']
        if segundo_apellido:
            _legislador.segundo_apellido = segundo_apellido
        #

        # Cargo
        _cargo = models.CargoLegislativo(0)
        _cargo.tipo_legislador_id = legislador['tipo']
        _cargo.region_id = legislador['region']
        _cargo.periodo_id = id_periodo
        _cargo.partido_politico_id = legislador['partido']
        _cargo.id_interna = legislador['id_interna']
        _cargo.circunscripcion = legislador.get('circunscripcion')

        distritos = legislador.get('distritos')
        if distritos:
            _cargo.distritos = legislador['distritos']
        else:
            _cargo.distritos = [legislador['distrito']]
        #

        _legislador.ultimo_tipo_legislador_id = legislador['tipo']
        _legislador.cargos = [_cargo]

        db.session.add(_legislador)
        legisladores_agregar.append(_legislador)

    print(f'Numero Legisladores a agregar = {len(legisladores_agregar)}')
    print('Legisladores:')
    for l in legisladores_agregar:
        print(l)
    if input('Agregar? (y) / (n) ').lower().strip() == 'y':
        db.session.commit()
        return True
    else:
        return False


# TODO
def actualizar_ingresar_senadores(db, lista_legisladores, id_periodo):
    """
    Actualizar legisladores

    Args:
        db (SQLAlchemy): ORM
        lista_legisladores (list): Diccionario con datos de los legisladores (obtenidos con su scrapper)
        id_periodo (int): El periodo legislativo de los legisladores.

    Returns:
        bool: Resultado de la operacion.

    """
    legisladores_agregar = []

    for legislador in lista_legisladores:
        # Legislador
        _legislador = models.Legislador(
            legislador['primer_nombre'],
            '',
            legislador['primer_apellido'],
            '',
            None,
            legislador['email'],
            legislador['telefono'],
            '',
            True,
            estado_noticioso_id=1,
        )
        segundo_nombre = legislador['segundo_nombre']
        if segundo_nombre:
            _legislador.segundo_nombre = segundo_nombre
        segundo_apellido = legislador['segundo_apellido']
        if segundo_apellido:
            _legislador.segundo_apellido = segundo_apellido
        #

        # Comparar legislador
        legislador_actualizar = models.Legislador.query.filter_by(
            primer_nombre=_legislador.primer_nombre,
            segundo_nombre=_legislador.segundo_nombre,
            primer_apellido=_legislador.primer_apellido,
            segundo_apellido=_legislador.segundo_apellido
        ).first()

        if legislador_actualizar:
            print('\nEl legislador existe en la base de datos')
            print(f'En sistema: {legislador_actualizar}')
            print(f'Encontrado: {_legislador}')

            telefono_nuevo = legislador['telefono']
            email_nuevo = legislador['email']

            if input('Actualizar? (y/n) ').lower().strip() == 'y':
                print('Comparando valores...')

                _legislador = legislador_actualizar
                db.session.expunge(legislador_actualizar)

                if _legislador.telefono != telefono_nuevo:
                    print('Telefono es distinto')
                    print(f'En sistema: {_legislador.telefono}')
                    print(f'Nuevo: {telefono_nuevo}')
                    if input('Actualizar? (y/n) ').lower().strip() == 'y':
                        _legislador.telefono = telefono_nuevo

                if _legislador.email != email_nuevo:
                    print('Email es distinto')
                    print(f'En sistema: {_legislador.email}')
                    print(f'Nuevo: {email_nuevo}')
                    if input('Actualizar? (y/n) ').lower().strip() == 'y':
                        _legislador.email = email_nuevo
        else:
            print('\nLegislador a agregar:')
            _legislador.print_to_console()
        #

        # Cargo
        _cargo = models.CargoLegislativo(0)
        _cargo.tipo_legislador = models.TipoLegislador.query.filter_by(id=legislador['tipo']).first()
        _cargo.region = models.Region.query.filter_by(id=legislador['region']).first()
        _cargo.periodo = models.Periodo.query.filter_by(id=id_periodo).first()
        _cargo.partido = models.PartidoPolitico.query.filter_by(id=legislador['partido']).first()
        _cargo.id_interna = legislador['id_interna']
        _cargo.circunscripcion = legislador.get('circunscripcion')

        distritos = legislador.get('distritos')
        if distritos:
            _cargo.distritos = legislador['distritos']
        else:
            _cargo.distritos = [legislador['distrito']]

        print('Cargo obtenido:')
        _cargo.print_to_console()

        db.session.add(_legislador)

        cargo_nuevo = True
        if legislador_actualizar:
            if input('TODO: Este cargo es nuevo? (y/n) ').lower().strip() == 'y':
                _legislador.cargos.append(_cargo)
                _legislador.ultimo_tipo_legislador_id = legislador['tipo']
            else:
                # TODO
                cargo_nuevo = False
        else:
            _legislador.cargos = [_cargo]
            _legislador.ultimo_tipo_legislador_id = legislador['tipo']
        #

        print('\nSumario:')
        _legislador.print_to_console()
        print(f'cargo nuevo = {cargo_nuevo}')
        print('=====================================')

        if input('Agregar? (y/n) ').lower().strip() == 'y':
            legisladores_agregar.append(_legislador)
        else:
            db.session.expunge(_legislador)


    print(f'Numero Legisladores a agregar = {len(legisladores_agregar)}')
    print('Legisladores:')
    for l in legisladores_agregar:
        print(l)
    if input('Confirmar cambios? (y/n) ').lower().strip() == 'y':
        db.session.commit()
        return True
    else:
        return False


if __name__ == '__main__':
    # Obtener periodos
    periodos = None
    try:
        periodos = models.Periodo.query.all()
    except exc.OperationalError as err:
        print(f'Error al conectar a la DB: {err}')
        quit()
    #

    # Obtener ids de periodos
    ids_periodos = [p.id for p in periodos]

    print("\nMantenedor - Project Snitch\n")

    # Variables de Control
    periodo_id = 0  # Periodo de los legisladores

    # Input accion a realizar
    acciones = {
        1: 'Actualizar e Ingresar legisladores',
        9999: 'Ingresar Legisladores por primera vez',
        'S': 'Salir'
    }

    for _k, _accion in acciones.items():
        print(f'[{_k}] {_accion}')

    accion = input('\nSeleccione accion a realizar: ').lower().strip()
    if accion == 's':
        print('Saliendo!')
        quit()
    #

    lista_legisladores = []

    lista_senadores = []
    lista_diputados = []

    # Imprimir lista de periodos
    print('Seleccione Periodo Legislativo de Legisladores: \n')
    for p in periodos:
        print(f'{p.id}._ {p} ')
    #

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
        LEGISLATURA_ANTIGUA = True
    print(f'Legislatura Antigua = {LEGISLATURA_ANTIGUA}')
    #

    # Desde archivo o web
    while True:
        fuente = str(input('Desde (A)rchivos o (W)eb? ')).lower().strip()

        if fuente == 'a':
            print('Cargando desde archivo')
            with open(DIR_JSON_DIPUTADOS, 'r', encoding='utf8') as _file:
                lista_diputados = json.load(_file)
            with open(DIR_JSON_SENADORES, 'r', encoding='utf8') as _file:
                lista_senadores = json.load(_file)
            print('Cargados')
            break

        if fuente == 'w':
            guardar = False
            if input('Guardar JSON legisladores? (y/n) ').lower().strip() == 'y':
                guardar = True

            print('\nObteniendo Legisladores\n')
            print('Diputados:')
            lista_diputados = get_lista_diputados()
            print()
            print('Senadores:')
            lista_senadores = get_lista_senadores()
            print()

            fecha = datetime.now()
            fecha_nombre = f'{fecha.year}-{fecha.month}-{fecha.day}'

            if guardar:
                print('Escribiendo a JSON')
                with open(f'senadores_{fecha_nombre}.json', 'w', encoding='utf8') as f:
                    json.dump(lista_senadores, f)
                with open(f'diputados_{fecha_nombre}.json', 'w', encoding='utf8') as f:
                    json.dump(lista_diputados, f)
                print('guardado Ok!')
            break
    #

    print('Creando Lista Maestra')
    lista_legisladores.extend(lista_diputados)
    lista_legisladores.extend(lista_senadores)

    print(f'Legisladores Obtenidos: {len(lista_legisladores)}')

    # Traducir datos
    print('Traduciendo datos')
    for legislador in lista_legisladores:
        region = legislador['region']
        partido = legislador['partido']

        if legislador['tipo'] == 'Senador':
            legislador['tipo'] = ID_TIPO_SENADOR
            legislador['region'] = TRADUCCION_REGIONES_SENADORES.get(region)
            legislador['partido'] = TRADUCCION_PARTIDOS_SENADORES.get(partido)

            # Circunscripcion a modelo
            num_circun = int(legislador['circunscripcion'])
            legislador['circunscripcion'] = models.Circunscripcion.query.\
                filter_by(numero=num_circun,
                          antiguo=LEGISLATURA_ANTIGUA).\
                first()

            # Distritos
            legislador['distritos'] = legislador['circunscripcion'].distritos

        else:
            legislador['tipo'] = ID_TIPO_DIPUTADO
            legislador['region'] = TRADUCCION_REGIONES_DIPUTADOS.get(region)
            legislador['partido'] = TRADUCCION_PARTIDOS_DIPUTADOS.get(partido)

            # Distrito a modelo
            num_distrito = int(legislador['distrito'])
            legislador['distrito'] = models.Distrito.query.\
                filter_by(numero=num_distrito,
                          antiguo=LEGISLATURA_ANTIGUA).\
                first()
    #

    if accion == '9999':
        # Ingresar legisladores al sistema
        print('\nIngresando al sistema por primera vez')
        resultado = ingresar_legisladores(db, lista_legisladores, periodo_id)
        print()
        if resultado:
            print('ok!')
        else:
            print('No se agregraron legisladores.')

    if accion == '1':
        print('\nActualizando Legisladores')
        resultado = actualizar_ingresar_senadores(db, lista_senadores, periodo_id)
        print()
        if resultado:
            print('ok!')
        else:
            print('No se agregraron legisladores.')

else:
    print('THIS IS NOT A MODULE')
    quit(0)
