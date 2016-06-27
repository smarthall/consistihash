import zlib
import hashlib

from collections import namedtuple
from bisect import bisect_left

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

def long_hash(iterations):
    def long_hash_impl(item):
        """
        This function should return a list numbers between 0 and pow(2, 32).
        """
        if type(item) == bytes:
            hash_bytes = item
        elif type(item) == str:
            hash_bytes = bytes(item, 'utf-8')
        else:
            hash_bytes = bytes(str(item), 'utf-8')

        digest_parts = []
        for i in range(iterations):
            digest_bytes = hashlib.sha512(hash_bytes).digest()
            hash_bytes = digest_bytes

            # Split into 4 byte sections
            digest_parts.extend(digest_bytes[i*4:(i+1)*4] for i in range(int(len(digest_bytes)/4)))

        return [int.from_bytes(part, byteorder='big') for part in digest_parts]

    return long_hash_impl


class Balancer(object):
    def __init__(self, servers, server_hash=long_hash(10), client_hash=short_hash):
        # Arguments
        self.servers = servers
        self._server_hash = server_hash
        self._client_hash = client_hash

        # Make ring
        self._make_server_ring()

    def add_server(self, server):
        self.servers.append(server)

        # Make ring
        self._make_server_ring()

    def _make_server_ring(self):
        servers = self.servers
        ring = []

        for server in servers:
            ids = self._server_hash(server)

            ring.extend((_ring_item(i, server) for i in ids))

        self._ring = sorted(ring, key=lambda x:x.id)
        self._ring_keys = list(map(lambda x:x.id, self._ring))

    def balance(self, client):
        client_id = self._client_hash(client)

        index = bisect_left(self._ring_keys, client_id)

        return self._ring[index % len(self._ring)]

