from bluetooth import Server
from time import sleep


def main():
    server = Server("b4:8c:9d:51:83:76", 4)
    server.connect()

    for i in range(30):
        print(i)
        sleep(1)

    server.deconnect()

    print("programme end")


if __name__ == "__main__":
    main()
