"""Guardado y carga de partidas, fragmentos y puntajes en la carpeta datos."""

import csv
import json
import os
from datetime import datetime

CARPETA_PROYECTO = os.path.dirname(os.path.abspath(__file__))
CARPETA_DATOS = os.path.join(CARPETA_PROYECTO, "datos")
RUTA_PARTIDA = os.path.join(CARPETA_DATOS, "partida.json")
RUTA_FRAGMENTOS = os.path.join(CARPETA_DATOS, "fragmentos.json")
RUTA_PUNTAJES = os.path.join(CARPETA_DATOS, "puntajes.csv")

COLUMNAS_PUNTAJES = ["nombre", "puntaje", "fragmentos_validos", "intentos", "fecha"]
NIVEL_MAXIMO = 6

# Errores posibles al leer un JSON que no existe, está dañado o fue alterado.
ERRORES_DE_LECTURA = (
    FileNotFoundError,
    json.JSONDecodeError,
    UnicodeDecodeError,
    KeyError,
    TypeError,
    OSError,
)


def escribir_json(ruta, datos):
    """Escribe datos en un archivo JSON y avisa si no se puede.

    Parámetros:
        ruta (str): ruta del archivo.
        datos (dict o list): información que se va a guardar.
    Devuelve:
        None.
    """
    nombre_archivo = os.path.basename(ruta)

    try:
        os.makedirs(CARPETA_DATOS, exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
    except PermissionError:
        print(f"Aviso: no hay permiso para escribir {nombre_archivo}.")
    except OSError:
        print(f"Aviso: no se pudo escribir {nombre_archivo}.")


def fragmento_valido(fragmento):
    """Comprueba que un fragmento tenga sus claves y tipos correctos.

    Parámetros:
        fragmento (dict): fragmento leído de un archivo.
    Devuelve:
        bool: True si el fragmento es válido.
    """
    return (
        isinstance(fragmento["codigo"], int)
        and isinstance(fragmento["titulo"], str)
        and isinstance(fragmento["sala"], str)
        and isinstance(fragmento["valor"], int)
        and isinstance(fragmento["principal"], bool)
    )


def partida_valida(estado):
    """Comprueba que una partida leída de un archivo se pueda jugar.

    Parámetros:
        estado (dict): estado leído del archivo.
    Devuelve:
        bool: True si el estado es válido.
    """
    jugador = estado["jugador"]
    inventario = estado["inventario"]
    intentos = estado["intentos_fallidos"]
    preguntas = estado["preguntas_ok"]

    datos_correctos = (
        isinstance(jugador["nombre"], str)
        and isinstance(jugador["vida"], int)
        and jugador["vida"] >= 0
        and isinstance(jugador["puntaje"], (int, float))
        and isinstance(jugador["nivel"], int)
        and 1 <= jugador["nivel"] <= NIVEL_MAXIMO
        and isinstance(jugador["catalogo_completo"], bool)
        and isinstance(inventario, list)
        and isinstance(intentos, int)
        and intentos >= 0
        and isinstance(preguntas, int)
        and preguntas >= 0
    )

    if not datos_correctos:
        return False

    for fragmento in inventario:
        if not fragmento_valido(fragmento):
            return False

    return True


def ubicaciones_a_tuplas(fragmentos):
    """Convierte a tupla la ubicación de los fragmentos que la tengan.

    JSON guarda las tuplas como listas, así que se reconvierten al cargar.

    Parámetros:
        fragmentos (list): lista de fragmentos; se modifica directamente.
    Devuelve:
        None.
    """
    for fragmento in fragmentos:
        if "ubicacion" in fragmento:
            fragmento["ubicacion"] = tuple(fragmento["ubicacion"])


def guardar_partida(estado):
    """Guarda el estado de la partida en datos/partida.json.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        None.
    """
    escribir_json(RUTA_PARTIDA, estado)


def cargar_partida():
    """Lee el estado de la partida desde datos/partida.json.

    Parámetros: ninguno.
    Devuelve:
        dict o None: estado guardado, o None si no existe o está dañado.
    """
    try:
        with open(RUTA_PARTIDA, "r", encoding="utf-8") as archivo:
            estado = json.load(archivo)

        if not partida_valida(estado):
            return None

        ubicaciones_a_tuplas(estado["inventario"])
        return estado
    except ERRORES_DE_LECTURA:
        return None


def guardar_fragmentos(inventario):
    """Guarda los fragmentos recolectados en datos/fragmentos.json.

    Parámetros:
        inventario (list): lista de fragmentos.
    Devuelve:
        None.
    """
    escribir_json(RUTA_FRAGMENTOS, inventario)


def cargar_fragmentos():
    """Lee los fragmentos desde datos/fragmentos.json.

    Parámetros: ninguno.
    Devuelve:
        list: fragmentos guardados; vacía si el archivo no existe o está dañado.
    """
    try:
        with open(RUTA_FRAGMENTOS, "r", encoding="utf-8") as archivo:
            fragmentos = json.load(archivo)

        if not isinstance(fragmentos, list):
            return []

        for fragmento in fragmentos:
            if not fragmento_valido(fragmento):
                return []

        ubicaciones_a_tuplas(fragmentos)
        return fragmentos
    except ERRORES_DE_LECTURA:
        return []


def contar_fragmentos_validos(inventario):
    """Cuenta los fragmentos del inventario sin tener en cuenta los duplicados.

    Parámetros:
        inventario (list): lista de fragmentos.
    Devuelve:
        int: cantidad de códigos distintos.
    """
    codigos = set()
    for fragmento in inventario:
        codigos.add(fragmento["codigo"])
    return len(codigos)


def registrar_puntaje(estado):
    """Agrega el resultado de la partida a datos/puntajes.csv.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        None.
    """
    fila = {
        "nombre": estado["jugador"]["nombre"],
        "puntaje": estado["jugador"]["puntaje"],
        "fragmentos_validos": contar_fragmentos_validos(estado["inventario"]),
        "intentos": estado["intentos_fallidos"],
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    try:
        os.makedirs(CARPETA_DATOS, exist_ok=True)
        archivo_nuevo = (
            not os.path.exists(RUTA_PUNTAJES)
            or os.path.getsize(RUTA_PUNTAJES) == 0
        )

        with open(RUTA_PUNTAJES, "a", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS_PUNTAJES)
            if archivo_nuevo:
                escritor.writeheader()
            escritor.writerow(fila)
    except PermissionError:
        print("Aviso: no hay permiso para escribir puntajes.csv.")
    except OSError:
        print("Aviso: no se pudo escribir puntajes.csv.")


def obtener_puntaje(fila):
    """Devuelve el puntaje de una fila; sirve como clave para ordenar.

    Parámetros:
        fila (dict): fila de la tabla de puntajes.
    Devuelve:
        float: puntaje de la fila.
    """
    return fila["puntaje"]


def leer_puntajes():
    """Lee los puntajes guardados en datos/puntajes.csv.

    Las filas dañadas se ignoran.

    Parámetros: ninguno.
    Devuelve:
        list: puntajes ordenados de mayor a menor; vacía si no hay archivo.
    """
    puntajes = []

    try:
        with open(RUTA_PUNTAJES, "r", newline="", encoding="utf-8") as archivo:
            for fila in csv.DictReader(archivo):
                try:
                    if None not in fila.values():
                        fila["puntaje"] = float(fila["puntaje"])
                        puntajes.append(fila)
                except (KeyError, ValueError):
                    continue
    except FileNotFoundError:
        return []
    except (csv.Error, UnicodeDecodeError, OSError):
        print("Aviso: no se pudo leer puntajes.csv.")
        return []

    puntajes.sort(key=obtener_puntaje, reverse=True)
    return puntajes
