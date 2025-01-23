from bluetooth_socket.request import Request
import socket

if not hasattr(socket, "AF_BLUETOOTH"):
    from bluetooth_socket.android_client import AndroidClient as Client
    Server = Client
else:
    from bluetooth_socket.client import Client
    from bluetooth_socket.server import Server

__all__ = (
    Request.__name__,
    Client.__name__,
    Server.__name__,
)
