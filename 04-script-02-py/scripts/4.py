#!/usr/bin/env python3

import sys
from subprocess import PIPE, Popen
import socket
import time
from datetime import datetime
port = "80"
timeout = "10"

hosts = ['drive.google.com','mail.google.com','google.com']
hosts_ip =['','','']
first = True
while True:
    now = datetime.now()
    print('\n')
    print('\033[37m' + now.strftime("%d/%m/%Y %H:%M:%S"))
    for index, host in enumerate(hosts):
        req = Popen('curl --write-out \'%{http_code}\' --silent --output /dev/null --connect-timeout ' + timeout + ' http://' + host + ':' + port, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = req.communicate()
        code = stdout.decode()
        now_ip = socket.gethostbyname(host)
        if not first:
            if now_ip.find(hosts_ip[index]) != -1:
                print('\033[32m' + host + ' - ' + now_ip + ' - HTTP code: ' + code)
            else:
                print('\033[31m[ERROR]' + host + ' IP mistmatch: ' + hosts_ip[index] + ' ' + now_ip + ' - HTTP code: ' + code)
                sys.exit(0)
        else:
            print('\033[32m' + host + ' - ' + now_ip + ' - HTTP code: ' + code)
        hosts_ip[index] = now_ip
    first = False
    time.sleep(5)
    
