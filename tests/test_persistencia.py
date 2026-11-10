"""Pruebas de guardado y carga de archivos en una carpeta temporal."""

import os
import tempfile
import unittest

import juego
import persistencia


class PruebasPersistencia(unittest.TestCase):
    """Pruebas de persistencia.py sin tocar los archivos reales de datos/."""

    def setUp(self):
        """Cambia las rutas del módulo a una carpeta temporal antes de cada prueba.

        Parámetros: ninguno.
        Devuelve: None.
        """
        self.temporal = tempfile.TemporaryDirectory()
        self.rutas_originales = (
            persistencia.CARPETA_DATOS,
            persistencia.RUTA_PARTIDA,
            persistencia.RUTA_FRAGMENTOS,
            persistencia.RUTA_PUNTAJES,
        )

        carpeta = os.path.join(self.temporal.name, "datos")
        persistencia.CARPETA_DATOS = carpeta
        persistencia.RUTA_PARTIDA = os.path.join(carpeta, "partida.json")
        persistencia.RUTA_FRAGMENTOS = os.path.join(carpeta, "fragmentos.json")
        persistencia.RUTA_PUNTAJES = os.path.join(carpeta, "puntajes.csv")

    def tearDown(self):
        """Restaura las rutas reales y borra la carpeta temporal.

        Parámetros: ninguno.
        Devuelve: None.
        """
        (
            persistencia.CARPETA_DATOS,
            persistencia.RUTA_PARTIDA,
            persistencia.RUTA_FRAGMENTOS,
            persistencia.RUTA_PUNTAJES,
        ) = self.rutas_originales
        self.temporal.cleanup()

    def crear_estado_ejemplo(self):
        """Crea un estado de partida con fragmentos para las pruebas.

        Parámetros: ninguno.
        Devuelve:
            dict: estado de ejemplo.
        """
        estado = juego.crear_estado("Lucía")
        estado["jugador"]["nivel"] = 3
        estado["inventario"] = [
            {"codigo": 412, "titulo": "Reglamento de préstamo", "sala": "Vestíbulo",
             "valor": 30, "principal": True},
            {"codigo": 731, "titulo": "Recibo de multa", "sala": "Vestíbulo",
             "valor": 15, "principal": False},
            {"codigo": 731, "titulo": "Recibo de multa", "sala": "Vestíbulo",
             "valor": 15, "principal": False},
        ]
        return estado

    def escribir_texto(self, ruta, texto):
        """Escribe un texto en un archivo, creando la carpeta si hace falta.

        Parámetros:
            ruta (str): ruta del archivo.
            texto (str): contenido.
        Devuelve:
            None.
        """
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(texto)

    def test_guardar_y_cargar_partida(self):
        """La partida cargada es igual a la guardada.

        Parámetros: ninguno.
        Devuelve: None.
        """
        estado = self.crear_estado_ejemplo()
        persistencia.guardar_partida(estado)
        self.assertEqual(persistencia.cargar_partida(), estado)

    def test_partida_inexistente(self):
        """Sin archivo, cargar_partida devuelve None.

        Parámetros: ninguno.
        Devuelve: None.
        """
        self.assertIsNone(persistencia.cargar_partida())

    def test_partida_danada(self):
        """Un JSON dañado o incompleto no lanza excepción y devuelve None.

        Parámetros: ninguno.
        Devuelve: None.
        """
        for contenido in ["", "{no es json", "[1, 2]", '{"jugador": {}}']:
            self.escribir_texto(persistencia.RUTA_PARTIDA, contenido)
            self.assertIsNone(persistencia.cargar_partida())

    def test_partida_en_nivel_siete(self):
        """Una partida terminada (nivel 7) se puede cargar.

        Parámetros: ninguno.
        Devuelve: None.
        """
        estado = self.crear_estado_ejemplo()
        estado["jugador"]["nivel"] = 7
        persistencia.guardar_partida(estado)
        self.assertEqual(persistencia.cargar_partida()["jugador"]["nivel"], 7)

    def test_guardar_y_cargar_fragmentos(self):
        """Los fragmentos cargados son iguales a los guardados.

        Parámetros: ninguno.
        Devuelve: None.
        """
        inventario = self.crear_estado_ejemplo()["inventario"]
        persistencia.guardar_fragmentos(inventario)
        self.assertEqual(persistencia.cargar_fragmentos(), inventario)

    def test_fragmentos_inexistentes_o_danados(self):
        """Sin archivo o con JSON dañado, cargar_fragmentos devuelve una lista vacía.

        Parámetros: ninguno.
        Devuelve: None.
        """
        self.assertEqual(persistencia.cargar_fragmentos(), [])
        self.escribir_texto(persistencia.RUTA_FRAGMENTOS, "{roto")
        self.assertEqual(persistencia.cargar_fragmentos(), [])

    def test_ubicacion_vuelve_como_tupla(self):
        """JSON guarda la ubicación como lista y al cargar vuelve a ser tupla.

        Parámetros: ninguno.
        Devuelve: None.
        """
        estado = self.crear_estado_ejemplo()
        estado["inventario"][0]["ubicacion"] = (1, 1)

        persistencia.guardar_fragmentos(estado["inventario"])
        persistencia.guardar_partida(estado)

        self.assertEqual(persistencia.cargar_fragmentos()[0]["ubicacion"], (1, 1))
        self.assertIsInstance(persistencia.cargar_fragmentos()[0]["ubicacion"], tuple)
        self.assertIsInstance(
            persistencia.cargar_partida()["inventario"][0]["ubicacion"], tuple
        )

    def test_puntajes_inexistentes(self):
        """Sin archivo de puntajes, leer_puntajes devuelve una lista vacía.

        Parámetros: ninguno.
        Devuelve: None.
        """
        self.assertEqual(persistencia.leer_puntajes(), [])

    def test_registrar_y_leer_puntajes_ordenados(self):
        """Los puntajes se leen de mayor a menor y con sus columnas.

        Parámetros: ninguno.
        Devuelve: None.
        """
        estado = self.crear_estado_ejemplo()
        for puntaje in [40.0, 95.5, 10.0]:
            estado["jugador"]["puntaje"] = puntaje
            persistencia.registrar_puntaje(estado)

        puntajes = persistencia.leer_puntajes()
        self.assertEqual([fila["puntaje"] for fila in puntajes], [95.5, 40.0, 10.0])
        self.assertEqual(puntajes[0]["nombre"], "Lucía")
        self.assertEqual(puntajes[0]["fragmentos_validos"], "2")

        with open(persistencia.RUTA_PUNTAJES, encoding="utf-8") as archivo:
            primera_linea = archivo.readline().strip()
        self.assertEqual(primera_linea, "nombre,puntaje,fragmentos_validos,intentos,fecha")


if __name__ == "__main__":
    unittest.main()
