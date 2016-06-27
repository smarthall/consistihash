#!/usr/bin/env python

import consistihash

import time
import uuid

from collections import Counter

# Settings
server_count = 4
client_count = 100000

# Create four servers
print("Generating Servers")
servers = [uuid.uuid4() for i in range(server_count)]

# Create several hundred clients
print("Generating Clients")
clients = [uuid.uuid4() for i in range(client_count)]

print("Generated %s servers for %s clients" % (len(servers), len(clients)))

# Create a consistent hash algorithm
for i in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]:
    hasher = consistihash.new(
        servers=servers,
        server_hash=consistihash.long_hash(i),
    )

    print("\n--- Server Hash Iterations %s ---" % i)
    tally = Counter()
    start = time.time()
    for c in clients:
        tally[hasher.balance(c)] += 1
    end = time.time()
    eachtime = (end - start) / len(clients) * 1000
    
    top = max(tally.values()) / len(clients)
    bot = min(tally.values()) / len(clients)
    imbalance = top - bot
    print("Imbalance factor: %s" % imbalance)
    print("Time per client: %sms" % eachtime)

