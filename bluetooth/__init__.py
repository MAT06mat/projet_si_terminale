import socket
from bluetooth.request import Request
from bluetooth.server import Server

if not hasattr(socket, "AF_BLUETOOTH"):
    from bluetooth.android_client import AndroidClient as Client
else:
    from bluetooth.client import Client

__all__ = (
    Request.__name__,
    Client.__name__,
    Server.__name__,
)
