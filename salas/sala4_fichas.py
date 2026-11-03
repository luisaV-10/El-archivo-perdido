"""Sala 4: Fichas (diccionarios)."""

from salas.sala3_mapas import HOJA_SUELTA as HOJA_DE_MAPAS
from utilidades import hacer_pregunta, pedir_entero, registrar_fallo

FICHERO = {
    142: {"titulo": "Cartas del puerto", "autor": "Rosa Pérez", "valor": 20},
    318: {"titulo": "Diccionario de signos", "autor": "Jorge Ríos"},
    507: {"titulo": "Crónicas de la ciudad", "valor": 35},
}
CAMPOS = ["titulo", "autor", "valor"]
CODIGO_REFERENCIA = 142

FRAGMENTO_PRINCIPAL = {
    "codigo": 253,
    "titulo": "Fichero de títulos",
    "sala": "Fichas",
    "valor": 35,
    "principal": True,
}
HOJA_SUELTA = {
    "codigo": 616,
    "titulo": "Ficha en blanco",
    "sala": "Fichas",
    "valor": 10,
    "principal": False,
}


def mostrar_ficha(codigo, ficha):
    """Muestra una ficha; los campos que no tiene aparecen como faltantes.

    Parámetros:
        codigo (int): código de la ficha.
        ficha (dict): datos de la ficha.
    Devuelve:
        None.
    """
    print(f"\nFicha {codigo}:")
    for campo in CAMPOS:
        print(f"  {campo}: {ficha.get(campo, '(falta)')}")


def consultar_fichas(fichero):
    """Deja consultar fichas por código hasta pedir una que exista y una que no.

    Las consultas no quitan vidas: una ficha inexistente solo genera un aviso.

    Parámetros:
        fichero (dict): diccionario {codigo: ficha}.
    Devuelve:
        None.
    """
    print("\nPaso 1: consulta fichas por código.")
    print("Pide al menos una que esté en el fichero y una que no esté.")

    pidio_existente = False
    pidio_inexistente = False

    while not (pidio_existente and pidio_inexistente):
        codigo = pedir_entero("Código a consultar: ")
        ficha = fichero.get(codigo)

        if ficha is None:
            print(f"Aviso: no hay ninguna ficha con el código {codigo}.")
            pidio_inexistente = True
        else:
            mostrar_ficha(codigo, ficha)
            pidio_existente = True


def encontrar_incompleta(estado, fichero):
    """Pide el código de la ficha que no tiene valor y lo verifica con in.

    Parámetros:
        estado (dict): estado de la partida.
        fichero (dict): diccionario {codigo: ficha}.
    Devuelve:
        int o None: código de la ficha sin valor, o None si se quedó sin vidas.
    """
    print("\nPaso 2: una de las fichas no tiene la clave «valor». ¿Cuál es?")

    while True:
        codigo = pedir_entero("Código de la ficha sin valor: ")

        if codigo not in fichero:
            print(f"Aviso: el código {codigo} no está en el fichero.")
        elif "valor" not in fichero[codigo]:
            print("Correcto: a esa ficha le falta el valor.")
            return codigo

        registrar_fallo(estado)
        if estado["jugador"]["vida"] <= 0:
            return None


def completar_valor(estado, fichero, codigo):
    """Pide el valor faltante de una ficha y lo agrega al diccionario.

    Parámetros:
        estado (dict): estado de la partida.
        fichero (dict): diccionario {codigo: ficha}; se modifica directamente.
        codigo (int): código de la ficha que se completa.
    Devuelve:
        bool: True si lo completó, False si se quedó sin vidas.
    """
    valor_correcto = fichero[CODIGO_REFERENCIA]["valor"] * 2

    print(f"\nPaso 3: su valor es el doble del valor de la ficha {CODIGO_REFERENCIA}.")

    while True:
        valor = pedir_entero("Valor faltante: ", 0)

        if valor == valor_correcto:
            fichero[codigo]["valor"] = valor
            print("Correcto: la ficha quedó así:")
            mostrar_ficha(codigo, fichero[codigo])
            return True

        registrar_fallo(estado)
        if estado["jugador"]["vida"] <= 0:
            return False


def entregar_fragmentos(estado):
    """Agrega al inventario el fragmento principal y dos hojas sueltas.

    La segunda hoja repite el código de una hoja de los Mapas para que la
    depuración con conjuntos tenga un duplicado que limpiar.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        None.
    """
    estado["inventario"].append(dict(FRAGMENTO_PRINCIPAL))
    estado["inventario"].append(dict(HOJA_SUELTA))
    estado["inventario"].append(dict(HOJA_DE_MAPAS))

    print(f"\nFragmento obtenido: {FRAGMENTO_PRINCIPAL['titulo']}")
    print(f"También recoges dos hojas sueltas: {HOJA_SUELTA['titulo']} y "
          f"{HOJA_DE_MAPAS['titulo']}")


def jugar(estado):
    """Ejecuta el reto de las Fichas y su pregunta conceptual.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        bool: True si se superó la sala, False si se acabaron las vidas.
    """
    print("\n=== Sala 4: Fichas ===")
    print("Encuentras un fichero: un diccionario que relaciona cada código con su ficha.")
    print("Algunas fichas quedaron incompletas.")

    fichero = {}
    for codigo in FICHERO:
        fichero[codigo] = dict(FICHERO[codigo])

    print("\nCódigos en el fichero:")
    for codigo in fichero:
        print(f"  {codigo}")

    consultar_fichas(fichero)

    codigo = encontrar_incompleta(estado, fichero)
    if codigo is None:
        return False

    if not completar_valor(estado, fichero, codigo):
        return False

    entregar_fragmentos(estado)

    hacer_pregunta(
        estado,
        '¿Cuál es la diferencia entre ficha["autor"] y ficha.get("autor")?',
        [
            "Ninguna: las dos lanzan un error si falta la clave",
            'ficha["autor"] lanza KeyError si falta la clave; ficha.get("autor") devuelve None',
            'ficha.get("autor") borra la clave después de leerla',
        ],
        1,
        "Con corchetes una clave inexistente detiene el programa; get no lo hace.",
    )

    return True
