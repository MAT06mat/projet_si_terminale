try:
    from mods import bluetooth_socket
except ModuleNotFoundError:
    import sys

    sys.path.insert(1, "\\".join(__file__.split("\\")[:-2]))
    from mods import bluetooth_socket

__all__ = bluetooth_socket
