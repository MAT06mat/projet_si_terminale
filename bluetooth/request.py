import json


class Request:
    callbacks = []
    REQUEST_LENGHT = 64

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
