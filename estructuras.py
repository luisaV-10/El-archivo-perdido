"""Árbol binario de búsqueda propio y funciones de apoyo para la Sala Central."""


class Nodo:
    """Representa un nodo del árbol binario de búsqueda.

    Atributos:
        fragmento (dict): fragmento completo que guarda el nodo.
        codigo (int): clave del nodo, tomada de fragmento["codigo"].
        izquierdo (Nodo o None): subárbol con los códigos menores.
        derecho (Nodo o None): subárbol con los códigos mayores.
    """

    def __init__(self, fragmento):
        """Crea un nodo sin hijos.

        Parámetros:
            fragmento (dict): fragmento que se guarda en el nodo.
        Devuelve:
            None.
        """
        self.fragmento = fragmento
        self.codigo = fragmento["codigo"]
        self.izquierdo = None
        self.derecho = None


class ArbolBusqueda:
    """Árbol binario de búsqueda cuya clave es el código del fragmento.

    En cada nodo, los códigos menores quedan a la izquierda y los mayores
    a la derecha.

    Atributos:
        raiz (Nodo o None): primer nodo del árbol.
        tamano (int): cantidad de nodos.
        altura (int): cantidad de niveles; un árbol vacío tiene altura 0.
    """

    def __init__(self):
        """Crea un árbol vacío.

        Parámetros: ninguno.
        Devuelve: None.
        """
        self.raiz = None
        self.tamano = 0
        self.altura = 0

    def esta_vacio(self):
        """Indica si el árbol no tiene nodos.

        Parámetros: ninguno.
        Devuelve:
            bool: True si el árbol está vacío.
        """
        return self.raiz is None

    def __len__(self):
        """Permite usar len(arbol) para saber cuántos nodos tiene.

        Parámetros: ninguno.
        Devuelve:
            int: cantidad de nodos.
        """
        return self.tamano

    def insertar(self, fragmento):
        """Inserta un fragmento usando su código como clave.

        Baja desde la raíz con un ciclo while: si el código es menor va a la
        izquierda y si es mayor va a la derecha, hasta encontrar un lugar vacío.

        Parámetros:
            fragmento (dict): fragmento con la clave "codigo".
        Devuelve:
            int: profundidad donde quedó el nodo (la raíz es 1),
                 o -1 si el código ya estaba en el árbol.
        """
        codigo = fragmento["codigo"]

        if self.raiz is None:
            self.raiz = Nodo(fragmento)
            self.tamano = 1
            self.altura = 1
            return 1

        actual = self.raiz
        profundidad = 1

        while True:
            if codigo == actual.codigo:
                return -1

            profundidad += 1

            if codigo < actual.codigo:
                if actual.izquierdo is None:
                    actual.izquierdo = Nodo(fragmento)
                    break
                actual = actual.izquierdo
            else:
                if actual.derecho is None:
                    actual.derecho = Nodo(fragmento)
                    break
                actual = actual.derecho

        self.tamano += 1
        if profundidad > self.altura:
            self.altura = profundidad
        return profundidad

    def buscar(self, codigo):
        """Busca un código bajando desde la raíz.

        Cuenta una comparación por cada nodo visitado.

        Parámetros:
            codigo (int): código que se busca.
        Devuelve:
            tuple: (fragmento o None, cantidad de comparaciones).
        """
        actual = self.raiz
        comparaciones = 0

        while actual is not None:
            comparaciones += 1

            if codigo == actual.codigo:
                return (actual.fragmento, comparaciones)
            elif codigo < actual.codigo:
                actual = actual.izquierdo
            else:
                actual = actual.derecho

        return (None, comparaciones)

    def inorden(self):
        """Recorre el árbol en inorden: izquierdo, nodo, derecho.

        Parámetros: ninguno.
        Devuelve:
            list: fragmentos ordenados de menor a mayor código.
        """
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, resultado):
        """Función auxiliar recursiva del recorrido inorden.

        Parámetros:
            nodo (Nodo o None): raíz del subárbol que se recorre.
            resultado (list): lista donde se agregan los fragmentos.
        Devuelve:
            None.
        """
        if nodo is None:
            return

        self._inorden(nodo.izquierdo, resultado)
        resultado.append(nodo.fragmento)
        self._inorden(nodo.derecho, resultado)

    def dibujar(self):
        """Dibuja el árbol rotado: la raíz a la izquierda y el subárbol derecho arriba.

        Cada línea tiene un código con sangría según su profundidad.

        Parámetros: ninguno.
        Devuelve:
            str: dibujo del árbol en texto.
        """
        if self.raiz is None:
            return "(árbol vacío)"

        lineas = []
        self._dibujar(self.raiz, 0, lineas)
        return "\n".join(lineas)

    def _dibujar(self, nodo, nivel, lineas):
        """Función auxiliar recursiva del dibujo.

        Parámetros:
            nodo (Nodo o None): raíz del subárbol que se dibuja.
            nivel (int): profundidad del nodo, empezando en 0.
            lineas (list): lista donde se agregan las líneas del dibujo.
        Devuelve:
            None.
        """
        if nodo is None:
            return

        self._dibujar(nodo.derecho, nivel + 1, lineas)
        lineas.append("      " * nivel + str(nodo.codigo))
        self._dibujar(nodo.izquierdo, nivel + 1, lineas)


def busqueda_secuencial(lista, codigo):
    """Busca un código recorriendo la lista desde el principio.

    Parámetros:
        lista (list): lista de fragmentos.
        codigo (int): código que se busca.
    Devuelve:
        tuple: (fragmento o None, cantidad de comparaciones).
    """
    comparaciones = 0

    for fragmento in lista:
        comparaciones += 1
        if fragmento["codigo"] == codigo:
            return (fragmento, comparaciones)

    return (None, comparaciones)


def esta_ordenada(codigos):
    """Comprueba que cada código sea menor que el siguiente.

    Compara los pares consecutivos con un ciclo, sin usar sorted.

    Parámetros:
        codigos (list): lista de enteros.
    Devuelve:
        bool: True si la lista está en orden estrictamente creciente.
    """
    for posicion in range(len(codigos) - 1):
        if codigos[posicion] >= codigos[posicion + 1]:
            return False
    return True
