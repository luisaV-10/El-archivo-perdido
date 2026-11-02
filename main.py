"""Punto de entrada de El Archivo Perdido. Se ejecuta con: python main.py"""

import juego


def main():
    """Inicia el juego y lo cierra con un aviso si se interrumpe la consola.

    Parámetros: ninguno.
    Devuelve: None.
    """
    try:
        juego.menu_principal()
    except (EOFError, KeyboardInterrupt):
        print("\nSe cerró la entrada de la consola. Hasta pronto.")


if __name__ == "__main__":
    main()
