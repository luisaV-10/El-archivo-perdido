"""Pruebas del puntaje y del estado de la partida en juego.py."""

import unittest

import juego

CODIGOS_PRINCIPALES = [412, 187, 645, 253, 839]


def crear_estado_con_principales(cantidad):
    """Crea un estado con cierta cantidad de fragmentos principales.

    Parámetros:
        cantidad (int): cuántos fragmentos principales tendrá el inventario.
    Devuelve:
        dict: estado de la partida.
    """
    estado = juego.crear_estado("Prueba")
    for codigo in CODIGOS_PRINCIPALES[:cantidad]:
        estado["inventario"].append({
            "codigo": codigo,
            "titulo": "Fragmento",
            "sala": "Sala",
            "valor": 10,
            "principal": True,
        })
    return estado


class PruebasPuntaje(unittest.TestCase):
    """Pruebas de calcular_puntaje en casos límite."""

    def test_partida_nueva(self):
        """Una partida nueva solo tiene los 10 puntos de las vidas.

        Parámetros: ninguno.
        Devuelve: None.
        """
        self.assertEqual(juego.calcular_puntaje(juego.crear_estado("Ana")), 10.0)

    def test_todo_perfecto_es_cien(self):
        """Cinco principales, seis preguntas y tres vidas dan 100.

        Parámetros: ninguno.
        Devuelve: None.
        """
        estado = crear_estado_con_principales(5)
        estado["preguntas_ok"] = 6
        self.assertEqual(juego.calcular_puntaje(estado), 100.0)

    def test_duplicados_no_suman(self):
        """Un principal repetido cuenta una sola vez.

        Parámetros: ninguno.
        Devuelve: None.
        """
        estado = crear_estado_con_principales(1)
        estado["inventario"].append(dict(estado["inventario"][0]))
        self.assertEqual(juego.calcular_puntaje(estado), 22.0)

    def test_preguntas_limitadas_a_treinta(self):
        """Más de seis preguntas no pasa de los 30 puntos ni de 100.

        Parámetros: ninguno.
        Devuelve: None.
        """
        estado = crear_estado_con_principales(5)
        estado["preguntas_ok"] = 20
        self.assertEqual(juego.calcular_puntaje(estado), 100.0)

    def test_muchos_intentos_fallidos_es_cero(self):
        """Con muchos intentos fallidos el puntaje es 0, nunca negativo.

        Parámetros: ninguno.
        Devuelve: None.
        """
        estado = juego.crear_estado("Prueba")
        estado["jugador"]["vida"] = 0
        estado["intentos_fallidos"] = 50
        puntaje = juego.calcular_puntaje(estado)
        self.assertEqual(puntaje, 0.0)
        self.assertIsInstance(puntaje, float)

    def test_siempre_entre_cero_y_cien(self):
        """En muchas combinaciones el puntaje queda entre 0 y 100.

        Parámetros: ninguno.
        Devuelve: None.
        """
        for principales in range(6):
            for preguntas in range(0, 10, 3):
                for vida in range(4):
                    for intentos in range(0, 60, 7):
                        estado = crear_estado_con_principales(principales)
                        estado["preguntas_ok"] = preguntas
                        estado["jugador"]["vida"] = vida
                        estado["intentos_fallidos"] = intentos
                        puntaje = juego.calcular_puntaje(estado)
                        self.assertGreaterEqual(puntaje, 0.0)
                        self.assertLessEqual(puntaje, 100.0)

    def test_redondeo_a_un_decimal(self):
        """El puntaje se redondea a un decimal.

        Parámetros: ninguno.
        Devuelve: None.
        """
        estado = crear_estado_con_principales(5)
        estado["preguntas_ok"] = 4
        estado["jugador"]["vida"] = 1
        estado["intentos_fallidos"] = 2
        self.assertEqual(juego.calcular_puntaje(estado), 79.3)


class PruebasPartidaTerminada(unittest.TestCase):
    """Pruebas de partida_terminada con la Sala Central."""

    def test_nivel_seis_sigue_en_la_sala_central(self):
        """Una partida en nivel 6 todavía se puede continuar.

        Parámetros: ninguno.
        Devuelve: None.
        """
        estado = juego.crear_estado("Prueba")
        estado["jugador"]["nivel"] = 6
        self.assertFalse(juego.partida_terminada(estado))

    def test_nivel_siete_o_sin_vidas_termina(self):
        """El nivel 7 o quedarse sin vidas termina la partida.

        Parámetros: ninguno.
        Devuelve: None.
        """
        estado = juego.crear_estado("Prueba")
        estado["jugador"]["nivel"] = 7
        self.assertTrue(juego.partida_terminada(estado))

        estado = juego.crear_estado("Prueba")
        estado["jugador"]["vida"] = 0
        self.assertTrue(juego.partida_terminada(estado))


if __name__ == "__main__":
    unittest.main()
