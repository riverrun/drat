# Authors: David Whitlock <alovedalongthe@gmail.com>
# A simple text analysis tool
# Copyright (C) 2013-2014 David Whitlock
#
# Drat is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Drat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Drat.  If not, see <http://www.gnu.org/licenses/gpl.html>.

import os
import argparse
import sys
import requests
from . import analysis, parsers

base_dir = '/usr/share' if os.path.isdir('/usr/share/drat') else '/usr/local/share'

usage_info = """The file, or url, you have chosen will be compared with a list of
common English words, and a report of the results will be saved in the current working directory.
You can also provide a list of url links (with each link on a separate line) written in a text file."""

def args_handler(args):
    """Handle the command line arguments."""
    if args.infile:
        exts = ('.docx', '.odt', '.ods', '.odp')
        for arg in args.infile:
            if arg.name.endswith(exts):
                doc_reader = parsers.DocParser(arg.name)
                data = doc_reader.get_doctype().splitlines()
                run_check(data, arg.name, args.wordlist)
            else:
                run_check(arg, arg.name, args.wordlist)
    if args.url:
        for arg in args.url:
            response = requests.get(arg)
            html = response.text
            url_reader = parsers.HtmlParser()
            url_reader.feed(html)
            data = url_reader.text
            run_check(data, arg, args.wordlist)

def run_check(data, name, wordlist):
    check = analysis.Checktext(name, wordlist, base_dir, False)
    check.load_file(data)

def main():
    parser = argparse.ArgumentParser(description='Text analysis tool', prog='drat', epilog=usage_info)
    parser.add_argument('-f', dest='infile', type=argparse.FileType('r'),
            nargs='+', help='Name of file(s) you want checked.')
    parser.add_argument('-l', dest='linklist', type=argparse.FileType('r'),
            nargs='+', help='Name of file with url link(s) you want checked.')
    parser.add_argument('-u', dest='url', type=str, nargs='+', help='Name of url(s) you want checked.')
    parser.add_argument('-w', dest='wordlist', type=argparse.FileType('r'),
            nargs='+', help='Name of additional wordlist(s) you want to use.')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    if args.linklist:
        args.url = [line.strip() for arg in args.linklist for line in arg]
    args_handler(args)
