# El Archivo Perdido

Juego serio por consola para practicar estructuras de datos en Python.

- **Integrante:** Luisa Fernanda Valencia
- **Asignatura:** Estructuras de Datos, Universidad de San Buenaventura, Medellín, 2026-2

## Cómo ejecutar

Requiere Python 3.11 o superior. No necesita paquetes externos.

```
python main.py
```

## Salas

| Sala | Estructura de datos | Descripción |
| --- | --- | --- |
| 1. Vestíbulo | Variables y tipos | Identificar los tipos del registro de un lector, convertirlos y calcular su multa. |
| 2. Estanterías | Listas | Retirar, insertar, buscar y ordenar los libros de una estantería derrumbada. |
| 3. Mapas | Tuplas | Predecir la casilla final de una ruta en una cuadrícula de 5×5. |
| 4. Fichas | Diccionarios | Consultar y completar las fichas de un fichero. |
| 5. Sellos | Conjuntos | Comparar sellos con diferencia, intersección y unión. |

La Sala Central se habilita en la próxima versión.

## Archivos que genera el juego

Se crean en la carpeta `datos/`:

- `partida.json`: partida guardada.
- `fragmentos.json`: fragmentos recolectados.
- `puntajes.csv`: resultados de las partidas.

## Estructura de módulos

```
main.py              Punto de entrada
juego.py             Menú, estado del jugador, recorrido de salas y puntaje
utilidades.py        Validación de entradas, fallos y preguntas
persistencia.py      Guardado y carga de archivos
estructuras.py       Nodo y ArbolBusqueda
salas/               Una sala por archivo
datos/               Archivos generados por el juego
```
