"""Sala 3: Mapas (tuplas)."""

from utilidades import hacer_pregunta, pedir_entero, registrar_fallo

TAMANO = 5
INICIO = (0, 0)
ESTANTES_CAIDOS = {(0, 3), (1, 3), (2, 2), (3, 0), (4, 3)}

# Cada movimiento es una tupla (filas, columnas) que se suma a la casilla actual.
DERECHA = (0, 1)
ABAJO = (1, 0)
NOMBRES_MOVIMIENTOS = {DERECHA: "derecha", ABAJO: "abajo"}
RUTA = [DERECHA, ABAJO, ABAJO, DERECHA, ABAJO, DERECHA, DERECHA]

FRAGMENTO_PRINCIPAL = {
    "codigo": 645,
    "titulo": "Plano de ubicación",
    "sala": "Mapas",
    "valor": 40,
    "principal": True,
}
HOJA_SUELTA = {
    "codigo": 269,
    "titulo": "Croquis del segundo piso",
    "sala": "Mapas",
    "valor": 20,
    "principal": False,
}


def mostrar_cuadricula(casilla_final=None):
    """Muestra el plano en texto.

    I es el inicio, X un estante caído, F la casilla final y . un pasillo libre.

    Parámetros:
        casilla_final (tuple o None): casilla que se marca con F, si se conoce.
    Devuelve:
        None.
    """
    print("\n    0 1 2 3 4")
    for fila in range(TAMANO):
        simbolos = []
        for columna in range(TAMANO):
            casilla = (fila, columna)
            if casilla == INICIO:
                simbolos.append("I")
            elif casilla == casilla_final:
                simbolos.append("F")
            elif casilla in ESTANTES_CAIDOS:
                simbolos.append("X")
            else:
                simbolos.append(".")
        print(f"  {fila} " + " ".join(simbolos))


def mostrar_ruta():
    """Muestra los movimientos de la ruta en orden.

    Parámetros: ninguno.
    Devuelve: None.
    """
    print("\nRuta:")
    for numero, movimiento in enumerate(RUTA, start=1):
        print(f"  {numero}. {NOMBRES_MOVIMIENTOS[movimiento]} {movimiento}")


def recorrer_ruta(ruta):
    """Recorre una ruta desempaquetando cada movimiento en fila y columna.

    Si el movimiento lleva a un estante caído, se permanece en la casilla.

    Parámetros:
        ruta (list): lista de tuplas de movimientos (filas, columnas).
    Devuelve:
        tuple: casilla final (fila, columna).
    """
    casilla = INICIO

    for fila, columna in ruta:
        siguiente = (casilla[0] + fila, casilla[1] + columna)
        if siguiente not in ESTANTES_CAIDOS:
            casilla = siguiente

    return casilla


def predecir_casilla(estado):
    """Pide al jugador la casilla final de la ruta y la compara con la real.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        bool: True si acertó, False si se quedó sin vidas.
    """
    casilla_final = recorrer_ruta(RUTA)

    while True:
        print("\n¿En qué casilla termina la ruta?")
        fila = pedir_entero("Fila: ", 0, TAMANO - 1)
        columna = pedir_entero("Columna: ", 0, TAMANO - 1)
        respuesta = (fila, columna)

        if respuesta == casilla_final:
            print(f"Correcto: la ruta termina en {casilla_final}.")
            mostrar_cuadricula(casilla_final)
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
    """Ejecuta el reto de los Mapas y su pregunta conceptual.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        bool: True si se superó la sala, False si se acabaron las vidas.
    """
    print("\n=== Sala 3: Mapas ===")
    print("Encuentras el plano de la biblioteca, una cuadrícula de 5×5.")
    print("Cada casilla es una tupla (fila, columna). Empiezas en (0, 0).")
    print("Si un movimiento lleva a un estante caído (X), te quedas donde estás.")

    mostrar_cuadricula()
    mostrar_ruta()

    if not predecir_casilla(estado):
        return False

    entregar_fragmentos(estado)

    hacer_pregunta(
        estado,
        "¿Por qué una coordenada se guarda en una tupla y no en una lista?",
        [
            "Porque una tupla es inmutable y puede guardarse en un conjunto",
            "Porque una tupla puede crecer con append",
            "Porque una lista no puede guardar números",
        ],
        0,
        "Una posición fija no debe cambiar, y solo lo inmutable entra en un conjunto.",
    )

    return True
