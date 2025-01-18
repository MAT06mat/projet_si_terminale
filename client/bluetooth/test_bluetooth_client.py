from bluetooth import Client, Request
from time import sleep


def main():
    client = Client()
    client.connect()

    client.send(Request.get("a", print))
    client.send(Request.get("b", print))
    client.send(Request.get("loop", print))
    client.send(Request.get("d", print))

    sleep(2)

    client.deconnect()

    print("progamme end")


if __name__ == "__main__":
    main()
