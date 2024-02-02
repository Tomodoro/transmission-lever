#!/usr/bin/env python

import json
from transmission_rpc import Client

f = open('../transmission-lever.json')

cfg = json.load(f)

client = Client(host=cfg["Client"]["host"],
                port=int(cfg["Client"]["port"]),
                username=cfg["Client"]["username"],
                password=cfg["Client"]["password"])

print(client.server_version)

torrents = client.get_torrents()

for torrent in torrents:
    print(torrent)