def jsonify(fn):
    def new_fn(*args, **kwargs):
        resp = fn(*args, **kwargs)
        return simplejson.loads(resp)
    return new_fn