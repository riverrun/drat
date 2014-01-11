# Authors: David Whitlock <alovedalongthe@gmail.com>
# A simple image viewer
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

import os.path
import argparse
import sys
import urllib.request
from . import analysis, parsers

base_dir = '/usr/share' if os.path.isdir('/usr/share/drat') else '/usr/local/share'

usage_info = """The file, or url, you have chosen will be compared with a list of
common English words, and a report of the results will be saved in the current working directory."""

def args_handler(args):
    if args.infile:
        for arg in args.infile:
            if arg.name.endswith(('.docx', '.odt', '.ods', '.odp')):
                doc_reader = parsers.DocParser(arg.name)
                data = doc_reader.get_doctype().splitlines()
                run_check(data, arg.name.split('.', 1)[0])
            else:
                run_check(arg, arg.name)
    if args.url:
        for arg in args.url:
            response = urllib.request.urlopen(arg)
            html = str(response.read())
            url_reader = parsers.HtmlParser()
            url_reader.feed(html)
            data = url_reader.text
            run_check(data, arg.rsplit('/', 1)[1])

def run_check(data, name):
    check = analysis.Checktext(name, base_dir)
    check.load_common()
    check.load_funcwords()
    check.load_file(data)

def main():
    parser = argparse.ArgumentParser(description='Text analysis tool', prog='drat', epilog=usage_info)
    parser.add_argument('-f', dest='infile', type=argparse.FileType('r'), nargs='+', help='Name of file you want checked.')
    parser.add_argument('-u', dest='url', type=str, nargs='+', help='Name of url you want checked.')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    args_handler(args)
