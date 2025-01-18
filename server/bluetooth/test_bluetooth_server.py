from bluetooth.bluetooth import Bluetooth
from time import sleep


def main():
    server = Bluetooth()
    server.server_connect()

    for i in range(3):
        print(i)
        sleep(1)

    server.server_deconnect()

    print("programme end")


if __name__ == "__main__":
    main()
