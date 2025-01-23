from backend.bluetooth_socket import Request
import socket

if not hasattr(socket, "AF_BLUETOOTH"):
    from backend.android_client import AndroidClient as Client
else:
    from backend.client import Client

__all__ = (
    Request.__name__,
    Client.__name__,
)
