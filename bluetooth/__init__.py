import socket
from bluetooth.request import Request
from bluetooth.server import Server

if hasattr(socket, "AF_BLUETOOTH"):
    from bluetooth.client import Client
else:
    from bluetooth.android_client import AndroidClient as Client

__all__ = (
    Request.__name__,
    Client.__name__,
    Server.__name__,
)
