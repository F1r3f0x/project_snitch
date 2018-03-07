"""
    Mantenedor Partidos Politicos
    Patricio Labin Correa (F1r3f0x) - 2017
    GPLv3
"""
from sistema.scrappers.partidos_politicos import get_partidos_politicos, URL_WIKI_LISTA_PP
import pymysql.cursors


# DB Variables
DB_HOST = 'example.net'
DB_PORT = 3306
DB_USER = 'user'  # Credenciales Aqui!!!
DB_PASS = 'pass'  # Y Aqui
DB_NAME = 'Snitch'
DB_CHARSET = 'utf8mb4'

if __name__ == '__main__':

    lista_partidos_nueva = get_partidos_politicos(URL_WIKI_LISTA_PP)

    if lista_partidos_nueva:
        print('Ok')

        conn = pymysql.connect(host=DB_HOST,
                        database=DB_NAME,
                        port=DB_PORT,
                        user=DB_USER,
                        password=DB_PASS,
                        charset=DB_CHARSET,
                        cursorclass=pymysql.cursors.DictCursor)

        with conn.cursor() as cursor:
            query = 'SELECT * FROM partido_politico'
            cursor.execute(query)
            lista_partidos_actual = cursor.fetchall()

            query = 'INSERT INTO Snitch.partido_politico (id, nombre, logo_url, activo) VALUES(%s, %s, "n/a", TRUE) ON DUPLICATE KEY UPDATE nombre=%s'

            for i, partido_nuevo in enumerate(lista_partidos_nueva):
                # Buscar si el partido existe y actualizar su logo
                for partido_actual in lista_partidos_actual:
                    if partido_nuevo['nombre'] in partido_actual.values():
                        # TODO: Actualizar Logo
                        print(f'{partido_nuevo["nombre"]} encontrado.')
                        lista_partidos_nueva.pop(i)

                print(f'{partido_nuevo["id"]} {partido_nuevo["nombre"]}')
                cursor.execute(query,
                               (partido_nuevo['id'],
                                partido_nuevo['nombre'],
                                partido_nuevo['nombre'])
                               )
            # TODO: generar lista de diferencias antes de hacer el commit
            conn.commit()
    else:
        print('fail :(')

else:
    print('THIS IS NOT A MODULE')
    quit(0)
