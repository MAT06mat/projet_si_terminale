from bluetooth import Client, Request
from time import sleep
import dotenv, os


def main():
    ADRESSE = os.getenv("ADRESSE")
    PORT = os.getenv("PORT")

    client = Client(ADRESSE, int(PORT))
    client.connect()

    client.send(Request.get("a", print))
    client.send(Request.get("b", print))
    client.send(Request.get("loop", print))
    client.send(Request.get("d", print))

    sleep(2)

    client.deconnect()

    print("progamme end")


if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
