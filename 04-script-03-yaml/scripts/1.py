#!/usr/bin/env python3

import sys
from subprocess import PIPE, Popen
import socket
import time
from datetime import datetime
import json
import yaml

port = "80"
timeout = "10"

hosts = {'drive.google.com':'','mail.google.com':'','google.com':''}

def update_hosts(hosts_l):
    for host in hosts_l:
        ip = socket.gethostbyname(host)
        hosts_l[host] = ip
    return hosts_l

def update_files(hosts_l):
    with open('hosts.json', 'w') as hosts_json:
        hosts_json.write(str(json.dumps(hosts_l)))
    with open('hosts.yaml', 'w') as hosts_yaml:
        hosts_yaml.write(yaml.dump(hosts_l))
    return

update_files(update_hosts(hosts))
now_hosts = update_hosts(hosts)
error = False

while True:
    now = datetime.now()
    print('\n')
    print('\033[37m' + now.strftime("%d/%m/%Y %H:%M:%S"))
    for index, host in enumerate(now_hosts):
        req = Popen('curl --write-out \'%{http_code}\' --silent --output /dev/null --connect-timeout ' + timeout + ' http://' + host + ':' + port, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = req.communicate()
        code = stdout.decode()
        now_ip = socket.gethostbyname(host)
        if now_ip.find(now_hosts[host]) != -1:
            print('\033[32m' + host + ' - ' + now_ip + ' - HTTP code: ' + code)
        else:
            print('\033[31m[ERROR]' + host + ' IP mistmatch: ' + now_hosts[host] + ' ' + now_ip + ' - HTTP code: ' + code)
            error = True
        
        now_hosts[host] = now_ip
    if error:
        update_files(now_hosts)
        sys.exit(0)
    time.sleep(5)
