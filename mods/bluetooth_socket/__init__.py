from mods.bluetooth_socket.request import Request
import socket

if not hasattr(socket, "AF_BLUETOOTH"):
    from mods.bluetooth_socket.android_client import AndroidClient as Client

    class Server:  # For no 'bluetooth' import error : no module name bluetooth
        pass

else:
    from mods.bluetooth_socket.client import Client
    from mods.bluetooth_socket.server import Server

__all__ = (
    Request.__name__,
    Client.__name__,
    Server.__name__,
)
