from bluetooth import *
import json, threading


class Request:
    callbacks = []
    REQUEST_LENGHT = 512

    def call(fname, *args):
        # Create a CALL request
        return Request.encode({"CALL": {"fname": fname, "args": args}})

    def get(var, callback):
        # Create a GET request and register the callback
        fid = id(callback)
        Request.callbacks.append((fid, callback))
        return Request.encode({"GET": {"var": var, "fid": fid}})

    def set(var, value):
        # Create a SET request
        return Request.encode({"SET": {"var": var, "value": value}})

    def encode(obj):
        # Encode the request as a JSON string and pad it to REQUEST_LENGHT
        binary = json.dumps(obj).encode("utf-8")
        fill = Request.REQUEST_LENGHT - len(binary)
        return binary + b"\x00" * fill

    def decode(obj):
        # Decode the JSON string, removing padding
        return json.loads(obj.rstrip(b"\x00").decode("utf-8"))

    def callback(fid, value):
        # Execute the callback function for the given fonction id
        for i in Request.callbacks:
            if i[0] == fid:
                Request.callbacks.remove(i)
                return i[1](value)


class Server:
    public_vars = ["callback"]
    uuid = "00001101-0000-1000-8000-00805F9B34FB"

    def __init__(self, bluetooth=True, request_lenght=512):

        # Set the request length for the Request class
        self.request_lenght = request_lenght
        Request.REQUEST_LENGHT = request_lenght

        # Initialize socket and connection variables
        self.socket = BluetoothSocket(RFCOMM)
        
        self.client = None
        self.is_server_connected = False

    def loop(self):
        print("Loop started")
        buffer = b""
        while True:
            try:
                # Accept client connection if server
                if not self.client:
                    self.client, addr = self.socket.accept()
                    print("Client socket accepted as", addr)
                # Receive data from client
                data = self.recv(self.request_lenght * 8)
                if data:
                    buffer += data
            except (ConnectionAbortedError, OSError) as e:
                if self.is_server_connected:
                    print("Client disconnected")
                    self.client = None
                    continue
                print("Loop stopped")
                return

            # Process received data
            while len(buffer) >= self.request_lenght:
                request = Request.decode(buffer[: self.request_lenght])
                buffer = buffer[self.request_lenght :]

                # Handle CALL requests
                if "CALL" in request:
                    if request["CALL"]["fname"] in self.public_vars:
                        func = self.__getattribute__(request["CALL"]["fname"])
                        func(*request["CALL"]["args"])

                # Handle GET requests
                if "GET" in request:
                    if request["GET"]["var"] in self.public_vars:
                        fid = request["GET"]["fid"]
                        value = self.__getattribute__(request["GET"]["var"])
                        response = Request.call("callback", fid, value)
                        self.send(response)

                # Handle SET requests
                if "SET" in request:
                    if request["SET"]["var"] in self.public_vars:
                        self.__setattr__(request["SET"]["var"], request["SET"]["value"])

    def callback(self, *args):
        # Handle callback
        Request.callback(*args)

    def recv(self, bufsize):
        return self.client.recv(bufsize)

    def send(self, request):
        # Send request to client or the server
        try:
            self.client.send(request)
        except ConnectionResetError:
            pass

    def connect(self):
        # Start server
        if self.is_server_connected:
            return
        self.is_server_connected = True
        self.socket.bind(("", PORT_ANY))
        self.socket.listen(1)
        advertise_service( self.socket, "SampleServer", service_id = self.uuid, service_classes = [ self.uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ])
        print("server-online")
        threading.Thread(target=self.loop).start()

    def deconnect(self):
        # Stop server
        if self.is_server_connected:
            self.is_server_connected = False
            if self.client:
                self.client.close()
            self.socket.close()
            print("server-offline")


if __name__ == '__main__':
    from time import sleep
    
    server = Server()
    server.connect()
    
    for i in range(4):
        print(i)
        sleep(10)
    
    server.deconnect()
