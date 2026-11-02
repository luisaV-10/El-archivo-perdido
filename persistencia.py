"""Guardado y carga de partidas, fragmentos y puntajes en la carpeta datos."""


def guardar_partida(estado):
    """Guarda el estado de la partida en datos/partida.json.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        None.
    """
    pass


def cargar_partida():
    """Lee el estado de la partida desde datos/partida.json.

    Parámetros: ninguno.
    Devuelve:
        dict o None: estado guardado, o None si no existe o está dañado.
    """
    pass


def guardar_fragmentos(inventario):
    """Guarda los fragmentos recolectados en datos/fragmentos.json.

    Parámetros:
        inventario (list): lista de fragmentos.
    Devuelve:
        None.
    """
    pass


def cargar_fragmentos():
    """Lee los fragmentos desde datos/fragmentos.json.

    Parámetros: ninguno.
    Devuelve:
        list: fragmentos guardados.
    """
    pass


def registrar_puntaje(estado):
    """Agrega el resultado de la partida a datos/puntajes.csv.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        None.
    """
    pass


def leer_puntajes():
    """Lee los puntajes guardados en datos/puntajes.csv.

    Parámetros: ninguno.
    Devuelve:
        list: puntajes ordenados de mayor a menor.
    """
    pass
