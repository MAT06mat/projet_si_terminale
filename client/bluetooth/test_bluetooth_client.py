from bluetooth.bluetooth import Bluetooth, Request
from time import sleep


def main():
    client = Bluetooth()
    client.client_connect()

    client.send(Request.get("d", print))

    sleep(1)

    client.client_deconnect()

    print("progamme end")


if __name__ == "__main__":
    main()
