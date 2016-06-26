import zlib
import hashlib

from collections import namedtuple

_ring_item = namedtuple('_ring_item', ['id', 'item'])

def short_hash(item):
    """
    This function should return a single number between 0 and pow(2, 32).
    """
    if type(item) == bytes:
        hash_bytes = item
    elif type(item) == str:
        hash_bytes = bytes(item, 'utf-8')
    else:
        hash_bytes = bytes(str(item), 'utf-8')

    return zlib.crc32(hash_bytes)

def long_hash(item):
    """
    This function should return a list numbers between 0 and pow(2, 32).
    """
    if type(item) == bytes:
        hash_bytes = item
    elif type(item) == str:
        hash_bytes = bytes(item, 'utf-8')
    else:
        hash_bytes = bytes(str(item), 'utf-8')

    digest_bytes = hashlib.sha512(hash_bytes).digest()

    # Split into 4 byte sections
    digest_parts = (digest_bytes[i*4:(i+1)*4] for i in range(int(len(digest_bytes)/4)))

    return [int.from_bytes(part, byteorder='big') for part in digest_parts]


class Balancer(object):
    def __init__(self, servers, server_hash=long_hash, client_hash=short_hash):
        # Arguments
        self.servers = servers
        self._server_hash = server_hash
        self._client_hash = client_hash

    def _make_server_ring(self):
        servers = self.servers
        ring = []

        for server in servers:
            ids = self._server_hash(server)

            ring.extend((_ring_item(i, server) for i in ids))

        return sorted(ring, key=lambda x:x.id)

    def balance(self, client):
        client_id = self._client_hash(client)
        ring = self._make_server_ring()

        index = 0

        while index < len(ring) and ring[index].id < client_id:
            index += 1

        return ring[index % len(ring)].item

