from bluetooth import Server
from time import sleep
import dotenv, os


def main():
    ADDRESSE = os.getenv("ADRESSE")
    PORT = os.getenv("PORT")

    server = Server(ADDRESSE, int(PORT), bluetooth=False)
    server.connect()

    for i in range(30):
        print(i)
        sleep(1)

    server.deconnect()

    print("programme end")


if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
