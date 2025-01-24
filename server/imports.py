try:
    from mods import bluetooth_socket
except ModuleNotFoundError:
    import sys

    sys.path.insert(
        1,
        "C:\\Users\\matth\\Documents\\Code\\Python\\Gros Projets\\projet_si_terminale",
    )
    from mods import bluetooth_socket

__all__ = bluetooth_socket
