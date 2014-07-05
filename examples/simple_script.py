#!/usr/bin/python3

import textwrap
from drat import app

with open('name_list.txt') as f:
    filenames = [line for line in f]

for arg in filenames:
    if arg.startswith(('http', 'ftp')):
        result = app.check_url(arg, None)
    else:
        result = app.check_file(arg, None)
    message = app.fmt_output(arg, False, *result)
    for line in message.splitlines():
        print(textwrap.fill(line, width=120))
    print('\n')
