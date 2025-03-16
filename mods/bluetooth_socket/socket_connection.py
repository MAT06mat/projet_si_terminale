from mods.bluetooth_socket.request import Request
from abc import ABC, abstractmethod
from threading import Thread


class SocketConnection(ABC):
    public_vars = {}
    is_server = False
    uuid = "00001101-0000-1000-8000-00805F9B34FB"

    def __init__(self, request_lenght=512):
        # Set the request length for the Request class
        self.request_lenght = request_lenght
        Request.REQUEST_LENGHT = request_lenght
        self.public_vars["callback"] = self.callback

    @abstractmethod
    def loop(self):
        pass

    def process_data(self, buffer):
        # Process received data
        while len(buffer) >= self.request_lenght:
            request = Request.decode(buffer[: self.request_lenght])
            buffer = buffer[self.request_lenght :]

            # Handle CALL requests
            if "CALL" in request:
                if request["CALL"]["fname"] in self.public_vars:
                    func = self.public_vars[request["CALL"]["fname"]]
                    Thread(target=lambda x: func(*request["CALL"]["args"]))

            # Handle GET requests
            if "GET" in request:
                if request["GET"]["var"] in self.public_vars:
                    fid = request["GET"]["fid"]
                    value = self.public_vars[request["GET"]["var"]]
                    response = Request.call("callback", fid, value)
                    try:
                        self.send(response)
                    except (ConnectionAbortedError, OSError) as e:
                        pass

            # Handle SET requests
            if "SET" in request:
                if request["SET"]["var"] in self.public_vars:
                    self.public_vars[request["SET"]["var"]] = request["SET"]["value"]

    def callback(self, *args):
        # Handle callback
        Request.callback(*args)

    @abstractmethod
    def send(self, request):
        pass
