import consistihash.hasher

from consistihash.hasher import long_hash, short_hash

def new(**kwargs):
    return hasher.Balancer(**kwargs)

