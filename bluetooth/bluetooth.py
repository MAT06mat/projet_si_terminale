import socket

ADRESSE = ""
PORT = 4


client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
client.connect((ADRESSE, PORT))
client.setblocking(False)

