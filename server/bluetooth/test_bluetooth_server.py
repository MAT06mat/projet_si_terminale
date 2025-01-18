from bluetooth import Server
from time import sleep


def main():
    server = Server()
    server.connect()

    for i in range(30):
        print(i)
        sleep(1)

    server.deconnect()

    print("programme end")


if __name__ == "__main__":
    main()
