import socket

client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
client.connect(("00:1a:7d:da:71:15", 4))

try:
    while True:
        message = input("New message : ")
        client.send(message.encode("utf-8"))
        data = client.recv(1024)
        if not data or data in ("break", "exit"):
            break
        print(f"Message -> {data.decode('utf-8')}")
except OSError as e:
    pass

client.close()