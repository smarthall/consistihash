#!/usr/bin/env python

import consistihash

import time
import uuid

from collections import Counter

# Settings
server_count = 4
client_count = 40000

# Create four servers
print("Generating Servers")
servers = [uuid.uuid4() for i in range(server_count)]

# Create several hundred clients
print("Generating Clients")
clients = [uuid.uuid4() for i in range(client_count)]

print("Generated %s servers for %s clients" % (len(servers), len(clients)))

# Create a consistent hash algorithm
hasher = consistihash.new(
    servers=servers,
)

# Balance the clients
print("Balancing clients")
tally = Counter()
total = 0
for c in clients:
    tally[hasher.balance(c)] += 1
    total += 1

# Print results
for item in tally:
    print("%s: %s" % (item, tally[item]/total))
