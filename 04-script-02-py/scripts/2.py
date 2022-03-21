#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
path_to_rep = os.popen('cd ~/netology/sysadm-homeworks && pwd').read().split('\n')[0]+('/')

is_change = False
print('\033[32mmodified:')
for result in result_os.split('\n'):
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
for result in result_os.split('\n'):
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
for result in result_os.split('\n'):
    if result.find('new file:') != -1:
        prepare_result = result.replace('\tnew file:   ', path_to_rep)
        print('\033[33m'+prepare_result)
        is_change = True
if not is_change:
    print('none')
