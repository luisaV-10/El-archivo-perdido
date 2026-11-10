"""Pruebas del árbol binario de búsqueda y de las funciones de estructuras.py."""

import random
import unittest

from estructuras import ArbolBusqueda, busqueda_secuencial, esta_ordenada


def crear_fragmento(codigo):
    """Crea un fragmento de prueba con el código indicado.

    Parámetros:
        codigo (int): código del fragmento.
    Devuelve:
        dict: fragmento con código y título.
    """
    return {"codigo": codigo, "titulo": f"Libro {codigo}"}


class PruebasArbolBusqueda(unittest.TestCase):
    """Pruebas de inserción, búsqueda, recorrido y altura del árbol."""

    def test_arbol_vacio(self):
        """Un árbol nuevo no tiene nodos, su altura es 0 y no encuentra nada.

        Parámetros: ninguno.
        Devuelve: None.
        """
        arbol = ArbolBusqueda()
        self.assertTrue(arbol.esta_vacio())
        self.assertEqual(len(arbol), 0)
        self.assertEqual(arbol.altura, 0)
        self.assertEqual(arbol.inorden(), [])
        self.assertEqual(arbol.buscar(412), (None, 0))

    def test_insertar_devuelve_profundidad(self):
        """La inserción devuelve la profundidad y actualiza tamaño y altura.

        Parámetros: ninguno.
        Devuelve: None.
        """
        arbol = ArbolBusqueda()
        profundidades = []
        for codigo in [412, 187, 645, 253, 839]:
            profundidades.append(arbol.insertar(crear_fragmento(codigo)))

        self.assertEqual(profundidades, [1, 2, 2, 3, 3])
        self.assertEqual(len(arbol), 5)
        self.assertEqual(arbol.altura, 3)
        self.assertFalse(arbol.esta_vacio())

    def test_buscar_existente(self):
        """Buscar un código existente devuelve su fragmento y las comparaciones.

        Parámetros: ninguno.
        Devuelve: None.
        """
        arbol = ArbolBusqueda()
        for codigo in [412, 187, 645, 253, 839]:
            arbol.insertar(crear_fragmento(codigo))

        fragmento, comparaciones = arbol.buscar(253)
        self.assertEqual(fragmento["codigo"], 253)
        self.assertEqual(comparaciones, 3)

        fragmento, comparaciones = arbol.buscar(412)
        self.assertEqual(comparaciones, 1)

    def test_buscar_inexistente(self):
        """Buscar un código que no está devuelve None.

        Parámetros: ninguno.
        Devuelve: None.
        """
        arbol = ArbolBusqueda()
        for codigo in [412, 187, 645]:
            arbol.insertar(crear_fragmento(codigo))

        fragmento, comparaciones = arbol.buscar(999)
        self.assertIsNone(fragmento)
        self.assertEqual(comparaciones, 2)

    def test_codigo_duplicado_devuelve_menos_uno(self):
        """Un código repetido no se inserta y no cambia el tamaño.

        Parámetros: ninguno.
        Devuelve: None.
        """
        arbol = ArbolBusqueda()
        arbol.insertar(crear_fragmento(412))
        arbol.insertar(crear_fragmento(187))

        self.assertEqual(arbol.insertar(crear_fragmento(187)), -1)
        self.assertEqual(len(arbol), 2)
        self.assertEqual(arbol.altura, 2)

    def test_inorden_ordenado_con_insercion_aleatoria(self):
        """Con inserción aleatoria, el inorden sale ordenado.

        Parámetros: ninguno.
        Devuelve: None.
        """
        generador = random.Random(7)
        codigos = generador.sample(range(1000, 10000), 200)

        arbol = ArbolBusqueda()
        for codigo in codigos:
            arbol.insertar(crear_fragmento(codigo))

        recorrido = [fragmento["codigo"] for fragmento in arbol.inorden()]
        self.assertEqual(recorrido, sorted(codigos))
        self.assertTrue(esta_ordenada(recorrido))
        self.assertEqual(len(arbol), 200)

    def test_altura_arbol_degenerado(self):
        """La inserción ascendente de n códigos da un árbol de altura n.

        Parámetros: ninguno.
        Devuelve: None.
        """
        arbol = ArbolBusqueda()
        for codigo in range(1, 51):
            arbol.insertar(crear_fragmento(codigo))

        self.assertEqual(arbol.altura, 50)
        self.assertEqual(arbol.buscar(50)[1], 50)

    def test_dibujar(self):
        """El dibujo pone la raíz sin sangría y el subárbol derecho arriba.

        Parámetros: ninguno.
        Devuelve: None.
        """
        arbol = ArbolBusqueda()
        self.assertEqual(arbol.dibujar(), "(árbol vacío)")

        for codigo in [412, 187, 645]:
            arbol.insertar(crear_fragmento(codigo))

        lineas = arbol.dibujar().split("\n")
        self.assertEqual([linea.strip() for linea in lineas], ["645", "412", "187"])
        self.assertEqual(lineas[1], "412")


class PruebasBusquedaSecuencial(unittest.TestCase):
    """Pruebas de la búsqueda secuencial."""

    def test_lista_vacia(self):
        """En una lista vacía no hay comparaciones.

        Parámetros: ninguno.
        Devuelve: None.
        """
        self.assertEqual(busqueda_secuencial([], 5), (None, 0))

    def test_un_elemento(self):
        """Con un elemento se hace una sola comparación.

        Parámetros: ninguno.
        Devuelve: None.
        """
        lista = [crear_fragmento(5)]
        self.assertEqual(busqueda_secuencial(lista, 5), (lista[0], 1))
        self.assertEqual(busqueda_secuencial(lista, 6), (None, 1))

    def test_varios_elementos(self):
        """Cuenta una comparación por elemento revisado.

        Parámetros: ninguno.
        Devuelve: None.
        """
        lista = [crear_fragmento(codigo) for codigo in [30, 10, 20]]
        fragmento, comparaciones = busqueda_secuencial(lista, 20)
        self.assertEqual(fragmento["codigo"], 20)
        self.assertEqual(comparaciones, 3)
        self.assertEqual(busqueda_secuencial(lista, 99), (None, 3))


class PruebasEstaOrdenada(unittest.TestCase):
    """Pruebas de la verificación de orden."""

    def test_vacia_y_un_elemento(self):
        """Una lista vacía o de un elemento está ordenada.

        Parámetros: ninguno.
        Devuelve: None.
        """
        self.assertTrue(esta_ordenada([]))
        self.assertTrue(esta_ordenada([7]))

    def test_ordenada(self):
        """Una lista creciente está ordenada.

        Parámetros: ninguno.
        Devuelve: None.
        """
        self.assertTrue(esta_ordenada([187, 253, 412, 645, 839]))

    def test_desordenada(self):
        """Una lista con un par fuera de orden no está ordenada.

        Parámetros: ninguno.
        Devuelve: None.
        """
        self.assertFalse(esta_ordenada([187, 412, 253]))
        self.assertFalse(esta_ordenada([5, 4]))

    def test_repetidos(self):
        """Dos códigos iguales seguidos no cumplen el orden estrictamente creciente.

        Parámetros: ninguno.
        Devuelve: None.
        """
        self.assertFalse(esta_ordenada([1, 2, 2, 3]))


if __name__ == "__main__":
    unittest.main()
