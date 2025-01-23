import json, socket


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


class SocketConnection:
    public_vars = ["callback"]
    uuid = "00001101-0000-1000-8000-00805F9B34FB"

    def __init__(self, address, port=4, request_lenght=512):
        self.address = address
        self.port = port

        # Set the request length for the Request class
        self.request_lenght = request_lenght
        Request.REQUEST_LENGHT = request_lenght

        # Initialize socket and connection variables
        if hasattr(socket, "AF_BLUETOOTH"):
            self.socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        else:
            self.socket = None
            self.recv_stream = None
            self.send_stream = None
        
        self.connected = False

    def loop(self):
        print("Loop started")
        buffer = b""
        while True:
            try:
                # Receive data from client
                data = self.recv(self.request_lenght * 8)
                if data:
                    buffer += data
            except (ConnectionAbortedError, OSError) as e:
                print("Loop stopped")
                self.connected = False
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
        return self.socket.recv(bufsize)

    def send(self, request):
        # Send request to the server
        try:
            self.socket.send(request)
        except ConnectionResetError:
            pass
