import json


class Request:
    callbacks = {}

    def call(fname, *args):
        return Request.encode({"CALL": {"fname": fname, "args": args}})

    def get(var, callback):
        fid = id(callback)
        Request.callbacks[fid] = callback
        return Request.encode({"GET": {"var": var, "fid": fid}})

    def set(var, value):
        return Request.encode({"SET": {"var": var, "value": value}})

    def encode(obj):
        return json.dumps(obj).encode("utf-8")

    def decode(obj):
        return json.loads(obj.decode("utf-8"))

    def callback(fid, value):
        callback = Request.callbacks[fid]
        del Request.callbacks[fid]
        return callback(value)
