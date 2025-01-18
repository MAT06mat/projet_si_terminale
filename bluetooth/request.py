import json


class Request:
    callbacks = []
    REQUEST_LENGHT = 64

    def call(fname, *args):
        return Request.encode({"CALL": {"fname": fname, "args": args}})

    def get(var, callback):
        fid = id(callback)
        Request.callbacks.append((fid, callback))
        return Request.encode({"GET": {"var": var, "fid": fid}})

    def set(var, value):
        return Request.encode({"SET": {"var": var, "value": value}})

    def encode(obj):
        binary = json.dumps(obj).encode("utf-8")
        fill = Request.REQUEST_LENGHT - len(binary)
        return binary + b"\x00" * fill

    def decode(obj):
        return json.loads(obj.rstrip(b"\x00").decode("utf-8"))

    def callback(fid, value):
        for i in Request.callbacks:
            if i[0] == fid:
                Request.callbacks.remove(i)
                return i[1](value)
