try:
    from mods import bluetooth_socket, analyser, solver
except ModuleNotFoundError:
    import sys

    sys.path.insert(
        1,
        "C:\\Users\\matth\\Documents\\Code\\Python\\Gros Projets\\projet_si_terminale",
    )
    from mods import bluetooth_socket, analyser, solver

__all__ = (bluetooth_socket.__name__, analyser.__name__, solver.__name__)
