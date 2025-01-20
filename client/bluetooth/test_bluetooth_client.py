from bluetooth import Client, Request
from time import sleep
import dotenv, os


def main():
    ADDRESSE = os.getenv("ADRESSE")
    PORT = os.getenv("PORT")

    client = Client(ADDRESSE, int(PORT), bluetooth=False)
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
