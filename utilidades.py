"""Funciones de apoyo compartidas por el juego y las salas."""


def pedir_entero(mensaje, minimo=None, maximo=None):
    """Pide un número entero hasta recibir uno válido.

    Parámetros:
        mensaje (str): texto que se muestra al pedir el dato.
        minimo (int o None): menor valor permitido; None si no hay límite.
        maximo (int o None): mayor valor permitido; None si no hay límite.
    Devuelve:
        int: número escrito por el jugador.
    """
    while True:
        texto = input(mensaje).strip()

        try:
            numero = int(texto)
        except ValueError:
            print("Debes escribir un número entero.")
            continue

        if minimo is not None and numero < minimo:
            print(f"El número debe ser mayor o igual a {minimo}.")
        elif maximo is not None and numero > maximo:
            print(f"El número debe ser menor o igual a {maximo}.")
        else:
            return numero


def pedir_texto(mensaje):
    """Pide un texto no vacío.

    Parámetros:
        mensaje (str): texto que se muestra al pedir el dato.
    Devuelve:
        str: texto escrito por el jugador, sin espacios en los extremos.
    """
    while True:
        texto = input(mensaje).strip()

        if texto != "":
            return texto

        print("Este dato no puede quedar vacío.")


def pedir_opcion(mensaje, opciones):
    """Muestra opciones numeradas y pide elegir una.

    Parámetros:
        mensaje (str): texto que se muestra al pedir la opción.
        opciones (list): textos de las opciones.
    Devuelve:
        int: posición de la opción elegida dentro de la lista (desde 0).
    """
    for numero, opcion in enumerate(opciones, start=1):
        print(f"{numero}. {opcion}")

    elegida = pedir_entero(mensaje, 1, len(opciones))
    return elegida - 1


def registrar_fallo(estado):
    """Resta una vida, suma un intento fallido e informa las vidas restantes.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        None.
    """
    jugador = estado["jugador"]
    jugador["vida"] = max(0, jugador["vida"] - 1)
    estado["intentos_fallidos"] += 1
    print(f"Respuesta incorrecta. Vidas restantes: {jugador['vida']}")


def hacer_pregunta(estado, enunciado, opciones, indice_correcto, explicacion=""):
    """Hace una pregunta conceptual de opción múltiple.

    Un acierto suma 1 a preguntas_ok. Un error no quita vida: solo muestra
    la respuesta correcta y su explicación.

    Parámetros:
        estado (dict): estado de la partida.
        enunciado (str): texto de la pregunta.
        opciones (list): textos de las opciones.
        indice_correcto (int): posición de la opción correcta (desde 0).
        explicacion (str): explicación de una línea de la respuesta correcta.
    Devuelve:
        bool: True si el jugador acertó.
    """
    print(f"\nPregunta: {enunciado}")
    elegida = pedir_opcion("Tu respuesta: ", opciones)

    if elegida == indice_correcto:
        estado["preguntas_ok"] += 1
        print("¡Correcto!")
        return True

    print(f"La respuesta correcta era: {opciones[indice_correcto]}")
    if explicacion != "":
        print(explicacion)
    return False
