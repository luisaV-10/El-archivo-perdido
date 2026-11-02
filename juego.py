"""Lógica general del juego: menú, estado del jugador, salas y puntaje."""

from salas import (
    sala1_vestibulo,
    sala2_estanterias,
    sala3_mapas,
    sala4_fichas,
    sala5_sellos,
)
from utilidades import pedir_opcion, pedir_texto

VIDAS_INICIALES = 3
SALAS = [
    sala1_vestibulo,
    sala2_estanterias,
    sala3_mapas,
    sala4_fichas,
    sala5_sellos,
]


def crear_estado(nombre):
    """Crea el estado inicial de una partida nueva.

    Parámetros:
        nombre (str): nombre del jugador.
    Devuelve:
        dict: estado de la partida con sus valores iniciales.
    """
    return {
        "jugador": {
            "nombre": nombre,
            "vida": VIDAS_INICIALES,
            "puntaje": 0.0,
            "nivel": 1,
            "catalogo_completo": False,
        },
        "inventario": [],
        "intentos_fallidos": 0,
        "preguntas_ok": 0,
    }


def contar_principales(estado):
    """Cuenta los fragmentos principales distintos del inventario.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        int: cantidad de códigos principales distintos.
    """
    codigos = set()
    for fragmento in estado["inventario"]:
        if fragmento["principal"]:
            codigos.add(fragmento["codigo"])
    return len(codigos)


def calcular_puntaje(estado):
    """Calcula el puntaje de la partida en una escala de 0 a 100.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        float: puntaje acotado entre 0 y 100, con 1 decimal.
    """
    puntos_fragmentos = min(12 * contar_principales(estado), 60)
    puntos_preguntas = min(5 * estado["preguntas_ok"], 30)
    puntos_vida = 10 * estado["jugador"]["vida"] / VIDAS_INICIALES
    penalizacion = 2 * estado["intentos_fallidos"]

    puntaje = puntos_fragmentos + puntos_preguntas + puntos_vida - penalizacion
    puntaje = max(0.0, min(puntaje, 100.0))
    return round(puntaje, 1)


def recorrer_salas(estado):
    """Juega en orden las salas pendientes desde la sala actual.

    Parámetros:
        estado (dict): estado de la partida; se actualiza sala por sala.
    Devuelve:
        bool: True si se terminaron las salas, False si la partida acabó antes.
    """
    jugador = estado["jugador"]

    while jugador["nivel"] <= len(SALAS):
        sala = SALAS[jugador["nivel"] - 1]
        superada = sala.jugar(estado)

        if not superada:
            return False

        jugador["nivel"] += 1
        jugador["puntaje"] = calcular_puntaje(estado)

    return True


def mostrar_resumen(estado):
    """Muestra los resultados de la partida.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        None.
    """
    jugador = estado["jugador"]
    print("\n--- Resumen de la partida ---")
    print(f"Jugador: {jugador['nombre']}")
    print(f"Fragmentos recolectados: {len(estado['inventario'])}")
    print(f"Fragmentos principales: {contar_principales(estado)} de {len(SALAS)}")
    print(f"Preguntas acertadas: {estado['preguntas_ok']}")
    print(f"Vidas restantes: {jugador['vida']}")
    print(f"Intentos fallidos: {estado['intentos_fallidos']}")
    print(f"Puntaje: {jugador['puntaje']}")


def terminar_partida(estado, salas_terminadas):
    """Calcula el puntaje final y muestra el cierre de la partida.

    Parámetros:
        estado (dict): estado de la partida.
        salas_terminadas (bool): True si se superaron todas las salas.
    Devuelve:
        None.
    """
    estado["jugador"]["puntaje"] = calcular_puntaje(estado)

    if salas_terminadas:
        print("\n¡Superaste las cinco salas del Archivo!")
    else:
        print("\nTe quedaste sin vidas. La partida termina aquí.")
        print("Repasa los temas de la sala donde te detuviste y vuelve a intentarlo.")

    mostrar_resumen(estado)

    if salas_terminadas:
        print("\nLa Sala Central se habilita en la próxima versión.")


def jugar_partida(estado):
    """Ejecuta una partida desde su sala actual hasta el final.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        None.
    """
    salas_terminadas = recorrer_salas(estado)
    terminar_partida(estado, salas_terminadas)


def nueva_partida():
    """Pide el nombre del jugador y empieza una partida nueva.

    Parámetros: ninguno.
    Devuelve: None.
    """
    nombre = pedir_texto("Escribe tu nombre: ")
    estado = crear_estado(nombre)
    jugar_partida(estado)


def menu_principal():
    """Muestra el menú principal hasta que el jugador decida salir.

    Parámetros: ninguno.
    Devuelve: None.
    """
    opciones = ["Nueva partida", "Cargar partida", "Ver puntajes", "Salir"]

    while True:
        print("\n=== EL ARCHIVO PERDIDO ===")
        opcion = pedir_opcion("Elige una opción: ", opciones)

        if opcion == 0:
            nueva_partida()
        elif opcion == 1 or opcion == 2:
            print("Esta opción se habilita cuando se conecte la persistencia.")
        else:
            print("Hasta pronto.")
            break
