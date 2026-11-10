"""Sala Central: La Reconstrucción del Catálogo (árbol binario de búsqueda)."""

import persistencia
from estructuras import ArbolBusqueda, busqueda_secuencial, esta_ordenada
from salas.sala2_estanterias import pedir_codigos
from utilidades import hacer_pregunta, pedir_entero, registrar_fallo

# Cada sala es un estante de la biblioteca.
ESTANTES = {"Vestíbulo": 1, "Estanterías": 2, "Mapas": 3, "Fichas": 4, "Sellos": 5}
CODIGOS_PRINCIPALES = [412, 187, 645, 253, 839]


def pausar():
    """Espera a que el jugador presione Enter para seguir.

    Parámetros: ninguno.
    Devuelve: None.
    """
    input("\nPresiona Enter para continuar...")


def mostrar_encabezado(numero, titulo):
    """Muestra el encabezado de un paso de la reconstrucción.

    Parámetros:
        numero (int): número del paso.
        titulo (str): nombre del paso.
    Devuelve:
        None.
    """
    print(f"\n--- Paso {numero}: {titulo} ---")


def paso_carga(estado):
    """Paso 1: lee los fragmentos desde datos/fragmentos.json.

    Si el archivo no existe o está dañado, usa el inventario de la partida
    como respaldo y vuelve a guardar el archivo.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        list: fragmentos cargados.
    """
    mostrar_encabezado(1, "Carga")
    fragmentos = persistencia.cargar_fragmentos()

    if len(fragmentos) == 0:
        print("Aviso: no se pudo leer fragmentos.json. Se usa el inventario de la partida.")
        fragmentos = [dict(fragmento) for fragmento in estado["inventario"]]
        persistencia.guardar_fragmentos(fragmentos)

    print(f"Se cargaron {len(fragmentos)} fragmentos.")
    return fragmentos


def depurar_fragmentos(fragmentos):
    """Deja solo la primera aparición de cada código usando un conjunto.

    Parámetros:
        fragmentos (list): fragmentos cargados, con posibles duplicados.
    Devuelve:
        tuple: (lista de fragmentos sin duplicados, conjunto de códigos repetidos).
    """
    codigos_vistos = set()
    repetidos = set()
    depurados = []

    for fragmento in fragmentos:
        codigo = fragmento["codigo"]
        if codigo in codigos_vistos:
            repetidos.add(codigo)
        else:
            codigos_vistos.add(codigo)
            depurados.append(fragmento)

    return (depurados, repetidos)


def paso_depuracion(fragmentos):
    """Paso 2: elimina los fragmentos duplicados e informa cuántos se descartaron.

    Parámetros:
        fragmentos (list): fragmentos cargados.
    Devuelve:
        list: fragmentos sin duplicados.
    """
    mostrar_encabezado(2, "Depuración")
    depurados, repetidos = depurar_fragmentos(fragmentos)
    descartados = len(fragmentos) - len(depurados)

    print(f"Se descartaron {descartados} fragmentos duplicados.")
    if len(repetidos) > 0:
        texto_repetidos = ", ".join(str(codigo) for codigo in sorted(repetidos))
        print(f"Códigos repetidos: {texto_repetidos}")
    print(f"Quedan {len(depurados)} fragmentos distintos.")
    return depurados


def asignar_ubicaciones(fragmentos):
    """Agrega a cada fragmento la tupla (estante, nivel).

    El estante es el número de su sala y el nivel es el orden en que
    aparece dentro de esa sala (1, 2, 3...).

    Parámetros:
        fragmentos (list): fragmentos sin duplicados; se modifican directamente.
    Devuelve:
        None.
    """
    cantidad_por_sala = {}

    for fragmento in fragmentos:
        sala = fragmento["sala"]
        estante = ESTANTES.get(sala, 0)
        nivel = cantidad_por_sala.get(sala, 0) + 1
        cantidad_por_sala[sala] = nivel
        fragmento["ubicacion"] = (estante, nivel)


def paso_ubicacion(fragmentos):
    """Paso 3: ubica cada fragmento en la biblioteca y guarda la lista.

    Parámetros:
        fragmentos (list): fragmentos sin duplicados.
    Devuelve:
        None.
    """
    mostrar_encabezado(3, "Ubicación")
    asignar_ubicaciones(fragmentos)

    print(f"{'Código':<8}{'Título':<28}{'Sala':<13}Ubicación")
    for fragmento in fragmentos:
        estante, nivel = fragmento["ubicacion"]
        print(
            f"{fragmento['codigo']:<8}{fragmento['titulo']:<28}"
            f"{fragmento['sala']:<13}estante {estante}, nivel {nivel}"
        )

    persistencia.guardar_fragmentos(fragmentos)


def paso_construccion(fragmentos):
    """Paso 4: inserta los fragmentos en un árbol binario de búsqueda.

    Parámetros:
        fragmentos (list): fragmentos sin duplicados, en el orden de carga.
    Devuelve:
        ArbolBusqueda: árbol con los fragmentos.
    """
    mostrar_encabezado(4, "Construcción")
    arbol = ArbolBusqueda()

    for fragmento in fragmentos:
        profundidad = arbol.insertar(fragmento)
        if profundidad == -1:
            print(f"El código {fragmento['codigo']} ya estaba en el árbol.")
        else:
            print(f"Código {fragmento['codigo']} insertado en la profundidad {profundidad}.")

    print("\nÁrbol (la raíz está a la izquierda y los mayores quedan arriba):\n")
    print(arbol.dibujar())
    print(f"\nTamaño: {len(arbol)} nodos. Altura: {arbol.altura} niveles.")
    return arbol


def primer_par_desordenado(codigos):
    """Busca el primer par de códigos consecutivos que está fuera de orden.

    Parámetros:
        codigos (list): lista de enteros.
    Devuelve:
        tuple o None: (código, siguiente código), o None si todo está en orden.
    """
    for posicion in range(len(codigos) - 1):
        if codigos[posicion] >= codigos[posicion + 1]:
            return (codigos[posicion], codigos[posicion + 1])
    return None


def paso_verificacion(estado, arbol, fragmentos):
    """Paso 5: reto del orden inorden y verificación del recorrido.

    Parámetros:
        estado (dict): estado de la partida.
        arbol (ArbolBusqueda): árbol construido.
        fragmentos (list): fragmentos sin duplicados, en el orden de carga.
    Devuelve:
        bool: True si se superó el paso, False si se quedó sin vidas.
    """
    mostrar_encabezado(5, "Verificación")
    recorrido = arbol.inorden()

    principales_cargados = [f["codigo"] for f in fragmentos if f["principal"]]
    principales_inorden = [f["codigo"] for f in recorrido if f["principal"]]

    if len(principales_cargados) > 0:
        texto = ", ".join(str(codigo) for codigo in principales_cargados)
        print(f"Fragmentos principales en el orden de carga: {texto}")
        print("Escríbelos en el orden en que saldrán del recorrido inorden.")

        acertado = False
        while not acertado:
            respuesta = pedir_codigos("Códigos separados por comas: ")
            if respuesta == principales_inorden:
                print("Correcto.")
                acertado = True
            else:
                registrar_fallo(estado)
                if estado["jugador"]["vida"] <= 0:
                    return False

    codigos = [fragmento["codigo"] for fragmento in recorrido]
    print(f"\nRecorrido inorden: {', '.join(str(codigo) for codigo in codigos)}")

    if esta_ordenada(codigos):
        print("Verificación correcta: el recorrido está ordenado de menor a mayor.")
    else:
        anterior, siguiente = primer_par_desordenado(codigos)
        print(f"Error: el recorrido NO está ordenado. {anterior} aparece antes que {siguiente}.")

    return True


def paso_consulta(estado, arbol, fragmentos):
    """Paso 6: búsquedas por código comparando el árbol con la búsqueda secuencial.

    Una búsqueda sin éxito suma un intento fallido, pero no quita vida.
    Para salir hay que haber hecho al menos una búsqueda exitosa.

    Parámetros:
        estado (dict): estado de la partida.
        arbol (ArbolBusqueda): árbol construido.
        fragmentos (list): fragmentos sin duplicados, para la búsqueda secuencial.
    Devuelve:
        None.
    """
    mostrar_encabezado(6, "Consulta")
    print("Busca fragmentos por código. Escribe 0 para terminar.")
    exitosas = 0

    while True:
        codigo = pedir_entero("\nCódigo a buscar: ", 0)

        if codigo == 0:
            if exitosas > 0:
                return
            print("Haz al menos una búsqueda exitosa antes de terminar.")
            continue

        fragmento, comparaciones_arbol = arbol.buscar(codigo)
        _, comparaciones_lista = busqueda_secuencial(fragmentos, codigo)
        conteo = f"árbol: {comparaciones_arbol} comparaciones | secuencial: {comparaciones_lista}"

        if fragmento is None:
            estado["intentos_fallidos"] += 1
            print(f"No existe el fragmento {codigo} | {conteo}")
        else:
            exitosas += 1
            print(f"Encontrado: {codigo} {fragmento['titulo']} | {conteo}")


def contar_principales_en_arbol(arbol):
    """Cuenta cuántos de los cinco códigos principales están en el árbol.

    Parámetros:
        arbol (ArbolBusqueda): árbol construido.
    Devuelve:
        int: cantidad de fragmentos principales encontrados.
    """
    encontrados = 0
    for codigo in CODIGOS_PRINCIPALES:
        fragmento, _ = arbol.buscar(codigo)
        if fragmento is not None:
            encontrados += 1
    return encontrados


def jugar(estado):
    """Ejecuta la Reconstrucción del Catálogo y su pregunta conceptual.

    Parámetros:
        estado (dict): estado de la partida.
    Devuelve:
        bool: True si se superó la sala, False si se acabaron las vidas.
    """
    print("\n=== Sala Central: La Reconstrucción del Catálogo ===")
    print("Llegas al centro de la biblioteca con los fragmentos que recogiste.")
    print("Con ellos vas a reconstruir el catálogo en seis pasos.")
    pausar()

    fragmentos = paso_carga(estado)
    if len(fragmentos) == 0:
        print("No hay fragmentos para reconstruir el catálogo.")
        return True
    pausar()

    depurados = paso_depuracion(fragmentos)
    pausar()

    paso_ubicacion(depurados)
    pausar()

    arbol = paso_construccion(depurados)
    pausar()

    if not paso_verificacion(estado, arbol, depurados):
        return False
    pausar()

    paso_consulta(estado, arbol, depurados)

    validos = contar_principales_en_arbol(arbol)
    print(f"\nFragmentos principales en el catálogo: {validos} de {len(CODIGOS_PRINCIPALES)}")

    hacer_pregunta(
        estado,
        "¿Por qué el recorrido inorden de un ABB entrega los códigos ordenados?",
        [
            "Porque los códigos siempre se insertan ya ordenados",
            "Porque visita izquierdo, nodo y derecho, y a la izquierda están los menores",
            "Porque Python ordena los nodos automáticamente",
            "Porque recorre el árbol nivel por nivel",
        ],
        1,
        "Todo lo menor queda a la izquierda de cada nodo, y inorden lo visita primero.",
    )

    if validos == len(CODIGOS_PRINCIPALES):
        estado["jugador"]["catalogo_completo"] = True
        print("\n¡El catálogo quedó completo!")

    return True
