"""Pruebas de la depuración y la ubicación de la Sala Central."""

import unittest

from salas.sala_central import (
    asignar_ubicaciones,
    depurar_fragmentos,
    primer_par_desordenado,
)


def crear_fragmentos_ejemplo():
    """Crea una lista de fragmentos con duplicados, como la que deja una partida.

    Parámetros: ninguno.
    Devuelve:
        list: fragmentos de ejemplo.
    """
    datos = [
        (412, "Vestíbulo", True),
        (731, "Vestíbulo", False),
        (731, "Vestíbulo", False),
        (187, "Estanterías", True),
        (528, "Estanterías", False),
        (731, "Vestíbulo", False),
        (645, "Mapas", True),
    ]
    fragmentos = []
    for codigo, sala, principal in datos:
        fragmentos.append({
            "codigo": codigo,
            "titulo": f"Fragmento {codigo}",
            "sala": sala,
            "valor": 10,
            "principal": principal,
        })
    return fragmentos


class PruebasDepuracion(unittest.TestCase):
    """Pruebas de depurar_fragmentos."""

    def test_elimina_duplicados(self):
        """Deja la primera aparición de cada código y reporta los repetidos.

        Parámetros: ninguno.
        Devuelve: None.
        """
        depurados, repetidos = depurar_fragmentos(crear_fragmentos_ejemplo())

        self.assertEqual([f["codigo"] for f in depurados], [412, 731, 187, 528, 645])
        self.assertEqual(repetidos, {731})

    def test_sin_duplicados(self):
        """Si no hay duplicados, la lista queda igual.

        Parámetros: ninguno.
        Devuelve: None.
        """
        fragmentos = crear_fragmentos_ejemplo()[:2]
        depurados, repetidos = depurar_fragmentos(fragmentos)
        self.assertEqual(depurados, fragmentos)
        self.assertEqual(repetidos, set())

    def test_lista_vacia(self):
        """Una lista vacía da una lista vacía y ningún repetido.

        Parámetros: ninguno.
        Devuelve: None.
        """
        self.assertEqual(depurar_fragmentos([]), ([], set()))


class PruebasUbicacion(unittest.TestCase):
    """Pruebas de asignar_ubicaciones."""

    def test_ubicacion_por_sala_y_orden(self):
        """El estante es el número de la sala y el nivel el orden dentro de ella.

        Parámetros: ninguno.
        Devuelve: None.
        """
        depurados, _ = depurar_fragmentos(crear_fragmentos_ejemplo())
        asignar_ubicaciones(depurados)

        ubicaciones = [f["ubicacion"] for f in depurados]
        self.assertEqual(ubicaciones, [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1)])
        self.assertIsInstance(ubicaciones[0], tuple)

    def test_sala_desconocida(self):
        """Una sala que no está en el diccionario queda en el estante 0.

        Parámetros: ninguno.
        Devuelve: None.
        """
        fragmentos = [{"codigo": 1, "titulo": "X", "sala": "Otra", "valor": 10,
                       "principal": False}]
        asignar_ubicaciones(fragmentos)
        self.assertEqual(fragmentos[0]["ubicacion"], (0, 1))


class PruebasPrimerParDesordenado(unittest.TestCase):
    """Pruebas de primer_par_desordenado."""

    def test_detecta_el_primer_par(self):
        """Devuelve el primer par fuera de orden, o None si todo está bien.

        Parámetros: ninguno.
        Devuelve: None.
        """
        self.assertEqual(primer_par_desordenado([1, 5, 3, 2]), (5, 3))
        self.assertIsNone(primer_par_desordenado([1, 2, 3]))


if __name__ == "__main__":
    unittest.main()
