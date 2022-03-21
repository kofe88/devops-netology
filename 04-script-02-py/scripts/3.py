#!/usr/bin/env python3

import sys
from sys import argv
import os
from subprocess import PIPE, Popen

if len (sys.argv) > 1:
    script,path = argv
else:
    path = os.getcwd()

print(path)
bash_command = ["cd " + path, "git status"]
#result_os = os.popen(' && '.join(bash_command)).read()

res_os = Popen(' && '.join(bash_command), shell=True, stdout=PIPE, stderr=PIPE)
stdout, stderr = res_os.communicate()

result_os = stdout
result_err = stderr
bash_path_command = ["cd " + path, "pwd"]
#path_to_rep = os.popen(' && '.join(bash_path_command)).read().split('\n')[0]+('/')

path_to_repo = Popen(' && '.join(bash_path_command), shell=True, stdout=PIPE, stderr=PIPE)
stdout_path, stderr_path = path_to_repo.communicate()
path_to_rep = stdout_path.decode().split('\n')[0]+('/')
path_to_repo_err = stderr_path.decode()
is_change = False

if path_to_repo_err.split('\n')[0].find('can\'t cd to') != -1:
    print('\033[31m'+path_to_repo_err)
    sys.exit(0)

if result_err.decode().split('\n')[0].find('fatal: not a git repository') != -1:
    print('\033[31m'+result_err.decode())
    sys.exit(0)

print('\033[32mmodified:')
for result in result_os.decode().split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', path_to_rep)
        print('\033[32m'+prepare_result)
        is_change = True
if not is_change:
    print('none')

flag = False
is_untracked = False
print('\033[31muntracked:')
str_num = 0
for result in result_os.decode().split('\n'):
    if result.find('Untracked') != -1:
        is_untracked = True
        flag = True
        str_num = str_num + 1
    elif flag:
        str_num = str_num + 1
        if str_num >= 3:
            if len(result) == 0:
                flag = False
            else:
                prepare_result = '\033[31m'+path_to_rep+result.strip()
                print(prepare_result)
if not is_untracked:
    print('none')

is_change = False
print('\033[33mnew file:')
for result in result_os.decode().split('\n'):
    if result.find('new file:') != -1:
        prepare_result = result.replace('\tnew file:   ', path_to_rep)
        print('\033[33m'+prepare_result)
        is_change = True
if not is_change:
    print('none')
