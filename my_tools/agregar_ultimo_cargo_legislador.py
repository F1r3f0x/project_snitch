"""
    Agrega id de ultimo tipo de cargo a los legisladores en el sistema
    Patricio Labin Correa - 2018
    GPLv3
"""
import pymysql.cursors

DB_HOST = 'example.net'
DB_HOST = 'example.net'
DB_PORT = 3306
DB_USER = 'user'  # Credenciales Aqui!!!
DB_PASS = 'pass'  # Y Aqui
DB_NAME = 'snitch'
DB_CHARSET = 'utf8mb4'


def agregar_ultimo_cargo():
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

        query_reemplazo = "UPDATE legislador SET ultimo_tipo_legislador_id=%s where id=%s"

        for legislador in legisladores:
            cur.execute('SELECT * from snitch.cargo_legislativo WHERE legislador_id = %s', (legislador['id'],))
            cargo = cur.fetchone()

            cur.execute(query_reemplazo, (cargo['tipo_legislador_id'], legislador['id']))

        conn.commit()

if __name__ == '__main__':
    agregar_ultimo_cargo()
    print('ok')