#!/usr/bin/env python3

import os
import sys
from subprocess import PIPE, Popen
import socket
import time
from datetime import datetime
import json
import yaml

port = "80" #порт который слушаем
timeout = "10" #таймаут подключения

hosts = {'drive.google.com':'','mail.google.com':'','google.com':''} #словарь "доменное имя" - "ip"

#функция заполнения словаря
def update_hosts(hosts_l):
    for host in hosts_l:
        ip = socket.gethostbyname(host)
        hosts_l[host] = ip
    return hosts_l

#функция обновления yaml и json
def update_files(hosts_l):
    with open('hosts.json', 'w') as hosts_json:
        hosts_json.write(str(json.dumps(hosts_l)))
    with open('hosts.yaml', 'w') as hosts_yaml:
        hosts_yaml.write(yaml.dump(hosts_l))
    return

#чтение из json файла
def load_file(hosts_l):
    if os.path.exists("hosts.json"):
        print("Read from file:")
        with open('hosts.json', 'r') as hosts_json:
            try:
                tmp_hosts = json.loads(hosts_json.read())
            except ValueError as err:
                print(err)
            for tmp_host in tmp_hosts:
                hosts_l[tmp_host] = tmp_hosts[tmp_host]
                print(tmp_host + " >>> " + hosts_l[tmp_host])
        return True
    else:
        return False


if load_file(hosts):
    now_hosts = hosts
    pass
else:
    print("No json file")
    update_files(update_hosts(hosts))
    now_hosts = update_hosts(hosts)
error = False

while True:
    now = datetime.now()
    print('\n')
    print('\033[37m' + now.strftime("%d/%m/%Y %H:%M:%S"))
    for index, host in enumerate(now_hosts):
        #подключаемся curl по ip и получаем ответ сервера
        req = Popen('curl --write-out \'%{http_code}\' --silent --output /dev/null --connect-timeout ' + timeout + ' http://' + host + ':' + port, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = req.communicate()
        code = stdout.decode()
        now_ip = socket.gethostbyname(host) #получаем текущий ip сервера
        if now_ip.find(now_hosts[host]) != -1:
            print('\033[32m' + host + ' - ' + now_ip + ' - HTTP code: ' + code)
        else:
            print('\033[31m[ERROR]' + host + ' IP mistmatch: ' + now_hosts[host] + ' >>> ' + now_ip + ' - HTTP code: ' + code)
            error = True
        
        now_hosts[host] = now_ip
    if error: #если ip сменился, записываем текущие ip в yaml и json, прерываем выполнение скрипта, но только после опроса всех 3х серверов
        update_files(now_hosts)
        sys.exit(0)
    time.sleep(5)
