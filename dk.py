#!/usr/bin/python

import json
import time
from docker import Client

c = Client(base_url='unix://var/run/docker.sock')

if len(c.images('busybox')) < 0:
    for line in c.pull('busybox', stream=True):
        print(json.dumps(json.loads(line), indent=4))

container = c.create_container(image="busybox:latest", command="sleep 30")
container_id = container['Id']
c.start(container_id)

inspect = c.inspect_container(container_id)

if inspect['State']['Running']:
    print "Container {} running".format(container_id)

time.sleep(2)

exec_id = c.exec_create(container_id, "ls -la")
out = c.exec_start(exec_id)
print out

c.remove_container(container_id, force=True)
