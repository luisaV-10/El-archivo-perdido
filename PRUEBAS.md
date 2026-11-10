# Pruebas manuales de robustez

Se hacen con `python main.py`. En ninguna el juego debe cerrarse ni mostrar un
error de Python (`Traceback`).

| # | Prueba | Cómo hacerla | Qué debe pasar |
| --- | --- | --- | --- |
| 1 | Letras donde va un número | En el menú escribe `abc` | «Debes escribir un número entero.» y vuelve a pedir la opción |
| 2 | Enter vacío | En el menú, o al pedir el nombre, presiona Enter sin escribir | Vuelve a pedir el dato; el nombre avisa «Este dato no puede quedar vacío.» |
| 3 | Opción fuera de rango | En el menú escribe `9` | «El número debe ser menor o igual a 4.» y vuelve a pedir |
| 4 | Cargar sin partida guardada | Borra `datos/partida.json` y elige la opción 2 | «No hay una partida guardada o el archivo está dañado.» y vuelve al menú |
| 5 | Ver puntajes sin archivo | Borra `datos/puntajes.csv` y elige la opción 3 | «Aún no hay puntajes.» |
| 6 | Sin `fragmentos.json` antes de la Sala Central | Juega hasta terminar la sala 5, sal del juego, borra `datos/fragmentos.json`, carga la partida | Continúa en la Sala Central; el paso 1 avisa que usa el inventario, carga 15 fragmentos y vuelve a crear el archivo |
| 7 | `partida.json` dañado | Abre `datos/partida.json`, borra la primera llave `{` y guarda; luego elige la opción 2 | «No hay una partida guardada o el archivo está dañado.» |
| 8 | `partida.json` con datos absurdos | Cambia `"nivel"` por `99` o `"vida"` por `"tres"` y carga | Lo trata como archivo dañado y vuelve al menú |
| 9 | Partida terminada | Termina una partida (completa o sin vidas) y elige la opción 2 | «La partida guardada ya terminó. Empieza una nueva.» |
| 10 | Respuesta inválida en un reto | En la Sala 3 escribe `x` como fila, o en la Sala Central escribe `abc` en la verificación | Vuelve a pedir el dato sin quitar vida |
| 11 | Búsqueda sin éxito en la Sala Central | En el paso 6 busca `999` | Dice que no existe y muestra las comparaciones; suma un intento fallido pero no quita vida |
| 12 | Salir sin búsqueda exitosa | En el paso 6 escribe `0` antes de encontrar algún código | Pide hacer al menos una búsqueda exitosa |
| 13 | Quedarse sin vidas | Falla tres veces seguidas en cualquier reto | Termina la partida, registra el puntaje parcial y muestra el resumen y la retroalimentación |
| 14 | Cerrar la entrada | Presiona Ctrl+C en cualquier momento | «Se cerró la entrada de la consola. Hasta pronto.» |

Pruebas automáticas: `python -m unittest discover -s tests -v`
