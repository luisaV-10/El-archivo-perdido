"""Sala 2: Estanterías (listas)."""

from salas.sala1_vestibulo import HOJA_SUELTA as HOJA_DEL_VESTIBULO
from utilidades import hacer_pregunta, pedir_entero, pedir_texto, registrar_fallo

LIBROS = [
    {"codigo": 304, "titulo": "Poemas de agua", "valor": 45},
    {"codigo": 118, "titulo": "Manual de redes", "valor": 60},
    {"codigo": 562, "titulo": "Diario mojado", "valor": 0},
    {"codigo": 276, "titulo": "Cuentos de mar", "valor": 55},
    {"codigo": 409, "titulo": "Atlas escolar", "valor": 30},
    {"codigo": 135, "titulo": "Historia de Antioquia", "valor": 75},
]
LIBRO_FALTANTE = {"codigo": 350, "titulo": "Mapas de Colombia", "valor": 50}
TITULO_VECINO = "Cuentos de mar"
CODIGO_BUSCADO = 409

FRAGMENTO_PRINCIPAL = {
    "codigo": 187,
    "titulo": "Índice de autores",
    "sala": "Estanterías",
    "valor": 25,
    "principal": True,
}
HOJA_SUELTA = {
    "codigo": 528,
    "titulo": "Etiqueta de estante",
    "sala": "Estanterías",
    "valor": 10,
    "principal": False,
}


def mostrar_estanteria(estanteria):
    """Muestra los libros con su posición en la lista.

    Parámetros:
        estanteria (list): lista de libros.
    Devuelve:
        None.
    """
    print("\nEstantería:")
    for posicion, libro in enumerate(estanteria):
        print(
            f"  [{posicion}] Código {libro['codigo']} | "
            f"{libro['titulo']} | Valor {libro['valor']}"
        )


def obtener_codigo(libro):
    """Devuelve el código de un libro; sirve como clave para ordenar.

    Parámetros:
        libro (dict): libro de la estantería.
    Devuelve:
        int: código del libro.
    """
    return libro["codigo"]


def buscar_danado(estanteria):
    """Busca el libro dañado, que es el que tiene valor 0.

    Parámetros:
        estanteria (list): lista de libros.
    Devuelve:
        dict: libro dañado.
    """
    for libro in estanteria:
        if libro["valor"] == 0:
            return libro


def retirar_danado(estado, estanteria):
    """Pide el código del libro dañado y lo retira con remove.

    Parámetros:
        estado (dict): estado de la partida.
        estanteria (list): lista de libros; se modifica directamente.
    Devuelve:
        bool: True si lo retiró, False si se quedó sin vidas.
    """
    danado = buscar_danado(estanteria)
    print("\nPaso 1: retira el libro dañado. Es el que quedó con valor 0.")

    while True:
        codigo = pedir_entero("Código del libro dañado: ")

        if codigo == danado["codigo"]:
            estanteria.remove(danado)
            print(f"Correcto: retiraste «{danado['titulo']}».")
            return True

        registrar_fallo(estado)
        if estado["jugador"]["vida"] <= 0:
            return False


def obtener_titulos(estanteria):
    """Crea una lista con los títulos de los libros en minúsculas.

    Parámetros:
        estanteria (list): lista de libros.
    Devuelve:
        list: títulos en minúsculas, en el mismo orden de la estantería.
    """
    return [libro["titulo"].lower() for libro in estanteria]


def insertar_faltante(estado, estanteria):
    """Pide la posición del libro faltante y lo agrega con insert.

    Parámetros:
        estado (dict): estado de la partida.
        estanteria (list): lista de libros; se modifica directamente.
    Devuelve:
        bool: True si lo insertó, False si se quedó sin vidas.
    """
    titulos = obtener_titulos(estanteria)
    posicion_correcta = titulos.index(TITULO_VECINO.lower()) + 1

    mostrar_estanteria(estanteria)
    print(f"\nPaso 2: falta «{LIBRO_FALTANTE['titulo']}».")
    print(f"Debe quedar justo después de «{TITULO_VECINO}».")

    while True:
        posicion = pedir_entero("Posición donde se inserta: ", 0, len(estanteria))

        if posicion == posicion_correcta:
            estanteria.insert(posicion, dict(LIBRO_FALTANTE))
            print("Correcto: el libro quedó en su lugar.")
            return True

        registrar_fallo(estado)
        if estado["jugador"]["vida"] <= 0:
            return False


def buscar_por_titulo(estado, estanteria):
    """Pide un título y lo busca en la lista con in e index.

    Parámetros:
        estado (dict): estado de la partida.
        estanteria (list): lista de libros.
    Devuelve:
        bool: True si lo encontró, False si se quedó sin vidas.
    """
    titulos = obtener_titulos(estanteria)

    mostrar_estanteria(estanteria)
    print(f"\nPaso 3: escribe el título del libro con código {CODIGO_BUSCADO}.")

    while True:
        titulo = pedir_texto("Título: ").lower()

        if titulo in titulos:
            posicion = titulos.index(titulo)
            print(f"Ese libro está en la posición {posicion}.")

            if estanteria[posicion]["codigo"] == CODIGO_BUSCADO:
                print("Correcto: es el libro que buscabas.")
                return True
        else:
            print("Ese título no está en la estantería.")

        registrar_fallo(estado)
        if estado["jugador"]["vida"] <= 0:
            return False


def pedir_codigos(mensaje):
    """Pide una lista de códigos separados por comas.

    Parámetros:
        mensaje (str): texto que se muestra al pedir el dato.
    Devuelve:
        list: códigos escritos por el jugador, como enteros.
    """
    while True:
        partes = pedir_texto(mensaje).split(",")

        try:
            return [int(parte) for parte in partes]
        except ValueError:
            print("Escribe solo números separados por comas.")


def ordenar_por_codigo(estado, estanteria):
    """Pide los códigos en orden y ordena la lista con sort y key.

    Parámetros:
        estado (dict): estado de la partida.
        estanteria (list): lista de libros; se modifica directamente.
    Devuelve:
        bool: True si acertó el orden, False si se quedó sin vidas.
    """
    orden_correcto = sorted([libro["codigo"] for libro in estanteria])

    print("\nPaso 4: escribe los códigos de menor a mayor, separados por comas.")

    while True:
        codigos = pedir_codigos("Códigos: ")

        if codigos == orden_correcto:
            estanteria.sort(key=obtener_codigo)
            print("Correcto: la estantería quedó ordenada.")
            mostrar_estanteria(estanteria)
            return True

        registrar_fallo(estado)
        if estado["jugador"]["vida"] <= 0:
            return False


def contar_valiosos(estado, estanteria):
    """Pide cuántos libros tienen valor mayor o igual a 50.

    Parámetros:
        estado (dict): estado de la partida.
        estanteria (list): lista de libros.
    Devuelve:
        bool: True si acertó, False si se quedó sin vidas.
    """
    valiosos = [libro for libro in estanteria if libro["valor"] >= 50]

    print("\nPaso 5: ¿cuántos libros tienen valor mayor o igual a 50?")

    while True:
        cantidad = pedir_entero("Cantidad: ", 0)

        if cantidad == len(valiosos):
            print("Correcto. Los libros valiosos son:")
            for libro in valiosos:
                print(f"  {libro['titulo']} (valor {libro['valor']})")
            return True

        registrar_fallo(estado)
        if estado["jugador"]["vida"] <= 0:
            return False


def entregar_fragmentos(estado):
    """Agrega al inventario el fragmento principal y dos hojas sueltas.

    La segunda hoja repite el código de una hoja del Vestíbulo para que la
    depuración con conjuntos tenga un duplicado que limpiar.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        None.
    """
    estado["inventario"].append(dict(FRAGMENTO_PRINCIPAL))
    estado["inventario"].append(dict(HOJA_SUELTA))
    estado["inventario"].append(dict(HOJA_DEL_VESTIBULO))

    print(f"\nFragmento obtenido: {FRAGMENTO_PRINCIPAL['titulo']}")
    print(f"También recoges dos hojas sueltas: {HOJA_SUELTA['titulo']} y "
          f"{HOJA_DEL_VESTIBULO['titulo']}")


def jugar(estado):
    """Ejecuta el reto de las Estanterías y su pregunta conceptual.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        bool: True si se superó la sala, False si se acabaron las vidas.
    """
    print("\n=== Sala 2: Estanterías ===")
    print("Una estantería se derrumbó y sus libros quedaron en desorden.")
    print("Organízalos para encontrar el siguiente fragmento del catálogo.")

    estanteria = [dict(libro) for libro in LIBROS]
    mostrar_estanteria(estanteria)

    if not retirar_danado(estado, estanteria):
        return False

    if not insertar_faltante(estado, estanteria):
        return False

    if not buscar_por_titulo(estado, estanteria):
        return False

    if not ordenar_por_codigo(estado, estanteria):
        return False

    if not contar_valiosos(estado, estanteria):
        return False

    entregar_fragmentos(estado)

    hacer_pregunta(
        estado,
        "¿Cuál es la diferencia entre lista.sort() y sorted(lista)?",
        [
            "Ninguna: las dos crean una lista nueva",
            "lista.sort() ordena la misma lista y sorted(lista) devuelve una nueva",
            "lista.sort() devuelve una lista nueva y sorted(lista) no devuelve nada",
        ],
        1,
        "sort() modifica la lista y devuelve None; sorted() deja la original igual.",
    )

    return True
