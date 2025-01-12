import socket

server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server.bind(("00:1a:7d:da:71:15", 4))
server.listen(1)


client, addr = server.accept()

try:
    while True:
        data = client.recv(1024)
        if not data or data in ("break", "exit"):
            break
        print(f"Message -> {data.decode('utf-8')}")
        message = input("Send : ")
        client.send(message.encode('utf-8'))
except OSError as e:
    pass

client.close()
server.close()