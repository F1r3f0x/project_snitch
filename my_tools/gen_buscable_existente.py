"""
    Generardor de texto buscable con legisladores preexistentes
    Patricio Labin Correa - 2017
    GPLv3
"""
import pymysql.cursors
from my_tools.funciones import get_texto_buscable

DB_HOST = 'example.net'
DB_PORT = 3306
DB_USER = 'user'  # Credenciales Aqui!!!
DB_PASS = 'pass'  # Y Aqui
DB_NAME = 'snitch'
DB_CHARSET = 'utf8mb4'


def gen_buscable_legisladores():
    """
    Genera texto_buscable para legisladores en la base de datos.
    """
    conn = pymysql.connect(host=DB_HOST,
                           port=DB_PORT,
                           user=DB_USER,
                           db=DB_NAME,
                           password=DB_PASS,
                           charset=DB_CHARSET,
                           cursorclass=pymysql.cursors.DictCursor)

    with conn.cursor() as cur:
        query = 'SELECT * FROM legislador'
        cur.execute(query)
        legisladores = cur.fetchall()

        query_reemplazo = "UPDATE legislador SET texto_buscable=%s where id=%s"

        for legislador in legisladores:
            texto_no_buscable = f"{legislador['primer_nombre']} {legislador['segundo_nombre']} {legislador['primer_apellido']} {legislador['segundo_apellido']}"
            texto_buscable = get_texto_buscable(texto_no_buscable)
            cur.execute(query_reemplazo, (texto_buscable, legislador['id']))

        conn.commit()

if __name__ == '__main__':
    gen_buscable_legisladores()
    print('ok')

