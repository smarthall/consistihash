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

# First balance
print("Balancing clients")
old = {}
oldtally = Counter()
for c in clients:
    s = hasher.balance(c)
    oldtally[s] += 1
    old[c] = s

# Add a new server
new_server = uuid.uuid4()
hasher.add_server(new_server)
print("Added new server: %s" % new_server)

# Second balance
print("Balancing clients")
new = {}
newtally = Counter()
for c in clients:
    s = hasher.balance(c)
    newtally[s] += 1
    new[c] = s

# Count reassignments
reassignments = 0
for c in clients:
    if old[c] != new[c]:
        reassignments += 1

total = len(clients)

# Print results
print("--- BEFORE ---")
for item in oldtally:
    print("%s: %s" % (item, oldtally[item] / total))

print("--- AFTER ---")
for item in newtally:
    print("%s: %s" % (item, newtally[item] / total))

print("--- OVERALL ---")
print("Reassignments: %s" % (reassignments / total))







