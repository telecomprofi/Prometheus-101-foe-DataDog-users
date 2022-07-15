#!/usr/bin/python3
import requests
import socket
import datetime
import time

res = requests.post("http://alertmanager:9093/api/v2/silences", json={
    "matchers": [
        {"name": "job", "value": "myjob", "isRegex": False},
        {"name": "instance", "value": "{}:1234".format(socket.gethostname()), "isRegex": False},
        ],
    "startsAt": datetime.datetime.utcfromtimestamp(time.time()).isoformat(),
    "endsAt": datetime.datetime.utcfromtimestamp(time.time() + 4*3600).isoformat(),
    "comment": "Backups on {}".format(socket.gethostname()),
    "createdBy": "My backup script",
    },
    )
res.raise_for_status()
silenceId = res.json()["silenceID"]
print(silenceId)
