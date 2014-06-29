#!/usr/bin/python3

from drat import application

with open('name_list.txt') as f:
    filenames = [line for line in f]

for arg in filenames:
    if arg.startswith(('http', 'ftp')):
        application.check_url(arg, None, False)
    else:
        application.check_file(arg, None, False)
    print('\n')
