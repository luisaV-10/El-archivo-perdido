"""Sala 1: Vestíbulo (variables y tipos)."""

from utilidades import hacer_pregunta, pedir_opcion, pedir_texto, registrar_fallo

REGISTRO = [
    {"campo": "Días de retraso", "texto": "7"},
    {"campo": "Multa por día", "texto": "1250.5"},
    {"campo": "Tiene carné", "texto": "True"},
    {"campo": "Nombre", "texto": "Ana"},
]
TIPOS = ["int", "float", "bool", "str"]

FRAGMENTO_PRINCIPAL = {
    "codigo": 412,
    "titulo": "Reglamento de préstamo",
    "sala": "Vestíbulo",
    "valor": 30,
    "principal": True,
}
HOJA_SUELTA = {
    "codigo": 731,
    "titulo": "Recibo de multa",
    "sala": "Vestíbulo",
    "valor": 15,
    "principal": False,
}


def convertir_texto(texto):
    """Convierte un texto del registro a su tipo real.

    La conversión a bool se hace comparando el texto, porque bool("False")
    es True: cualquier texto que no esté vacío se considera verdadero.

    Parámetros:
        texto (str): dato del registro.
    Devuelve:
        bool, int, float o str: dato convertido.
    """
    if texto == "True" or texto == "False":
        return texto == "True"

    try:
        return int(texto)
    except ValueError:
        pass

    try:
        return float(texto)
    except ValueError:
        return texto


def mostrar_registro():
    """Muestra el registro del último lector, con todos sus datos como texto.

    Parámetros: ninguno.
    Devuelve: None.
    """
    print("\nRegistro del último lector:")
    for dato in REGISTRO:
        print(f'  {dato["campo"]}: "{dato["texto"]}"')


def identificar_tipos(estado):
    """Pide al jugador el tipo correcto de cada dato del registro.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        bool: True si identificó todos los tipos, False si se quedó sin vidas.
    """
    for dato in REGISTRO:
        valor = convertir_texto(dato["texto"])
        tipo_correcto = type(valor).__name__
        acertado = False

        while not acertado:
            print(f'\n¿Qué tipo debe tener "{dato["texto"]}" ({dato["campo"]})?')
            elegida = pedir_opcion("Tipo: ", TIPOS)

            if TIPOS[elegida] == tipo_correcto:
                print(f"Correcto: {dato['campo']} = {valor!r} ({tipo_correcto})")
                acertado = True
            else:
                registrar_fallo(estado)
                if estado["jugador"]["vida"] <= 0:
                    return False

    return True


def pedir_decimal(mensaje):
    """Pide un número decimal hasta recibir uno válido.

    Parámetros:
        mensaje (str): texto que se muestra al pedir el dato.
    Devuelve:
        float: número escrito por el jugador.
    """
    while True:
        texto = pedir_texto(mensaje)

        try:
            return float(texto.replace(",", "."))
        except ValueError:
            print("Debes escribir un número, por ejemplo 100.5")


def calcular_multa(estado):
    """Pide al jugador la multa total y la compara con el valor real.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        bool: True si la calculó bien, False si se quedó sin vidas.
    """
    dias = convertir_texto(REGISTRO[0]["texto"])
    multa_por_dia = convertir_texto(REGISTRO[1]["texto"])
    multa_total = dias * multa_por_dia

    print("\nEl torniquete pide la multa total: días de retraso × multa por día.")

    while True:
        respuesta = pedir_decimal("Multa total: ")

        if abs(respuesta - multa_total) < 0.01:
            print("Correcto. El torniquete se abre.")
            return True

        registrar_fallo(estado)
        if estado["jugador"]["vida"] <= 0:
            return False


def entregar_fragmentos(estado):
    """Agrega al inventario el fragmento principal y dos hojas sueltas.

    La segunda hoja repite el código de la primera para que la depuración
    con conjuntos tenga un duplicado que limpiar.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        None.
    """
    estado["inventario"].append(dict(FRAGMENTO_PRINCIPAL))
    estado["inventario"].append(dict(HOJA_SUELTA))
    estado["inventario"].append(dict(HOJA_SUELTA))

    print(f"\nFragmento obtenido: {FRAGMENTO_PRINCIPAL['titulo']}")
    print(f"También recoges dos hojas sueltas: {HOJA_SUELTA['titulo']}")


def jugar(estado):
    """Ejecuta el reto del Vestíbulo y su pregunta conceptual.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        bool: True si se superó la sala, False si se acabaron las vidas.
    """
    print("\n=== Sala 1: Vestíbulo ===")
    print("El catálogo de la biblioteca fue destruido y debes reconstruirlo.")
    print("Un torniquete bloquea la entrada: su registro quedó guardado como texto.")
    print("Indica el tipo de cada dato y calcula la multa para poder pasar.")

    mostrar_registro()

    if not identificar_tipos(estado):
        return False

    if not calcular_multa(estado):
        return False

    entregar_fragmentos(estado)

    hacer_pregunta(
        estado,
        '¿Qué ocurre con int("2.5") y cómo se evita que el juego se detenga?',
        [
            "Devuelve 2; no hace falta hacer nada",
            "Lanza ValueError; se evita con try/except y volviendo a pedir el dato",
            "Devuelve 2.5 como float; se evita usando str()",
        ],
        1,
        "int() no acepta textos con punto decimal, y try/except atrapa el error.",
    )

    return True
