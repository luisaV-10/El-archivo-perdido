"""Sala 5: Sellos (conjuntos)."""

from salas.sala4_fichas import HOJA_SUELTA as HOJA_DE_FICHAS
from utilidades import hacer_pregunta, pedir_entero, pedir_texto, registrar_fallo

SELLOS_OFICIALES = {"llave", "sol", "pluma", "torre", "luna", "rosa"}
DOCUMENTO_1 = ["llave", "sol", "llave", "pluma", "sol"]
DOCUMENTO_2 = ["sol", "torre", "pluma", "torre", "luna"]

FRAGMENTO_PRINCIPAL = {
    "codigo": 839,
    "titulo": "Registro de sellos",
    "sala": "Sellos",
    "valor": 45,
    "principal": True,
}
HOJA_SUELTA = {
    "codigo": 974,
    "titulo": "Sello roto",
    "sala": "Sellos",
    "valor": 10,
    "principal": False,
}


def mostrar_documentos():
    """Muestra los sellos de cada documento antes y después de depurarlos con set().

    Parámetros: ninguno.
    Devuelve: None.
    """
    print(f"\nSellos oficiales: {', '.join(sorted(SELLOS_OFICIALES))}")

    print(f"\nDocumento 1, tal como llegó: {DOCUMENTO_1}")
    print(f"Documento 1 sin repetidos:   {sorted(set(DOCUMENTO_1))}")

    print(f"\nDocumento 2, tal como llegó: {DOCUMENTO_2}")
    print(f"Documento 2 sin repetidos:   {sorted(set(DOCUMENTO_2))}")


def pedir_conjunto(mensaje):
    """Pide sellos separados por comas y los devuelve como conjunto.

    No importan el orden, los espacios ni las mayúsculas.

    Parámetros:
        mensaje (str): texto que se muestra al pedir el dato.
    Devuelve:
        set: sellos escritos por el jugador.
    """
    while True:
        partes = pedir_texto(mensaje).split(",")
        sellos = set()

        for parte in partes:
            sello = parte.strip().lower()
            if sello != "":
                sellos.add(sello)

        if len(sellos) > 0:
            return sellos

        print("Escribe al menos un sello.")


def resolver_con_conjunto(estado, enunciado, respuesta_correcta):
    """Pide una respuesta como conjunto hasta que sea correcta.

    Parámetros:
        estado (dict): estado de la partida.
        enunciado (str): pregunta que se muestra al jugador.
        respuesta_correcta (set): sellos que forman la respuesta.
    Devuelve:
        bool: True si acertó, False si se quedó sin vidas.
    """
    print(f"\n{enunciado}")

    while True:
        respuesta = pedir_conjunto("Sellos separados por comas: ")

        if respuesta == respuesta_correcta:
            print("Correcto.")
            return True

        registrar_fallo(estado)
        if estado["jugador"]["vida"] <= 0:
            return False


def contar_distintos(estado, total_correcto):
    """Pide cuántos sellos distintos hay entre los dos documentos.

    Parámetros:
        estado (dict): estado de la partida.
        total_correcto (int): tamaño de la unión de los dos documentos.
    Devuelve:
        bool: True si acertó, False si se quedó sin vidas.
    """
    print("\nPaso 3: ¿cuántos sellos distintos hay entre los dos documentos?")

    while True:
        cantidad = pedir_entero("Cantidad: ", 0)

        if cantidad == total_correcto:
            print("Correcto.")
            return True

        registrar_fallo(estado)
        if estado["jugador"]["vida"] <= 0:
            return False


def entregar_fragmentos(estado):
    """Agrega al inventario el fragmento principal y dos hojas sueltas.

    La segunda hoja repite el código de una hoja de las Fichas para que la
    depuración con conjuntos tenga un duplicado que limpiar.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        None.
    """
    estado["inventario"].append(dict(FRAGMENTO_PRINCIPAL))
    estado["inventario"].append(dict(HOJA_SUELTA))
    estado["inventario"].append(dict(HOJA_DE_FICHAS))

    print(f"\nFragmento obtenido: {FRAGMENTO_PRINCIPAL['titulo']}")
    print(f"También recoges dos hojas sueltas: {HOJA_SUELTA['titulo']} y "
          f"{HOJA_DE_FICHAS['titulo']}")


def jugar(estado):
    """Ejecuta el reto de los Sellos y su pregunta conceptual.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        bool: True si se superó la sala, False si se acabaron las vidas.
    """
    print("\n=== Sala 5: Sellos ===")
    print("Dos documentos llevan sellos de autenticidad, pero algunos se repiten.")
    print("Usa los conjuntos para saber cuáles son auténticos.")

    sellos_1 = set(DOCUMENTO_1)
    sellos_2 = set(DOCUMENTO_2)

    faltantes = SELLOS_OFICIALES - sellos_1
    compartidos = sellos_1 & sellos_2
    todos = sellos_1 | sellos_2

    mostrar_documentos()

    if not resolver_con_conjunto(
        estado, "Paso 1: ¿qué sellos oficiales le faltan al documento 1?", faltantes
    ):
        return False

    if not resolver_con_conjunto(
        estado, "Paso 2: ¿qué sellos comparten los dos documentos?", compartidos
    ):
        return False

    if not contar_distintos(estado, len(todos)):
        return False

    print(f"Los sellos distintos son: {', '.join(sorted(todos))}")

    entregar_fragmentos(estado)

    hacer_pregunta(
        estado,
        "¿Por qué un conjunto no permite acceder a sus elementos por índice?",
        [
            "Porque no tiene orden: sus elementos no ocupan posiciones fijas",
            "Porque solo puede guardar números",
            "Porque es inmutable, igual que una tupla",
        ],
        0,
        "Un conjunto no guarda posiciones, así que no existe un elemento [0] o [1].",
    )

    return True
