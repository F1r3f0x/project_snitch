"""
    Utilidades para vista
    Patricio Labin Correa - 2017
    GPLv3
"""


def string_distritos(lista_distritos: list):
    """
    Devuelve una string formateada con todos los distritos en la lista
    ej: "1, 4, 10 y 25"

    Args:
        lista_distritos (list): Lista con los distritos

    Returns:
        str: String con lista de Distritos.
    """

    if len(lista_distritos) <= 1:
        return str(lista_distritos[0].numero)

    # Tomar todos los numeros de distritos
    numero_distritos = []

    # Unir todos menos el ultimo
    for d in lista_distritos[:-1]:
        numero_distritos.append(str(d.numero))
    distritos = ", ".join(numero_distritos)

    # Unir el ultimo
    distritos += ' y ' + str(lista_distritos[-1].numero)

    return distritos


def get_last_dir_url(next_url: str):
    """
    Devuelve el ultimo miembro de una URL
    Args:
        next_url (str): url a recorrer.

    Returns:
        str: Ultimo miembro de next_url

    """
    for i in range(len(next_url) - 1, -1, -1):
        if next_url[i] == '/':
            return next_url[i+1:]
