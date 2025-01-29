try:
    from mods import bluetooth_socket, analyser, solver
except ModuleNotFoundError:
    import sys

    sys.path.insert(1, "\\".join(__file__.split("\\")[:-2]))
    from mods import bluetooth_socket, analyser, solver

__all__ = (bluetooth_socket.__name__, analyser.__name__, solver.__name__)
