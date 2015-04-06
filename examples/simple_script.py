#!/usr/bin/python3
# A simple script that takes a text file with a list of filenames in it
# and then analyzes these text files.

import textwrap
from drat import app

with open('name_list.txt') as f:
    filenames = [line for line in f]

for arg in filenames:
    message = app.start_check(arg, None, False)
    for line in message.splitlines():
        print(textwrap.fill(line, width=120))
