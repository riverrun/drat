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

import os.path
import argparse
import sys
import requests
from . import analysis, parsers

usage_info = """The file, or url, you have chosen will be compared with a list of
common English words, and a report of the results will be saved in the current working directory.
You can also provide a list of url links (with each link on a separate line) written in a text file."""

class ArgsHandler(object):
    """Handle the command line arguments."""
    def __init__(self, args):
        self.args = args
        if not args.infile:
            with sys.stdin as f:
                data = f.read()
            self.args.infile = [arg for arg in data.splitlines()]

    def args_handler(self, base_dir):
        for arg in self.args.infile:
            if arg.startswith('http'):
                self.check_url(arg, base_dir)
            else:
                self.check_file(arg, base_dir)

    def check_url(self, arg, base_dir):
        response = requests.get(arg)
        html = response.text
        url_reader = parsers.HtmlParser()
        url_reader.feed(html)
        data = url_reader.text
        self.run_check(data, arg, self.args.wordlist, base_dir)

    def check_file(self, arg, base_dir):
        exts = ('.docx', '.odt', '.ods', '.odp')
        if arg.endswith(exts):
            doc_reader = parsers.DocParser(arg)
            data = doc_reader.get_doctype().splitlines()
        else:
            with open(arg) as f:
                data = f.read().splitlines()
        self.run_check(data, arg, self.args.wordlist, base_dir)

    def run_check(self, data, name, wordlist, base_dir):
        check = analysis.Checktext(name, wordlist, base_dir, False)
        check.load_file(data)

def main():
    base_dir = '/usr/share' if os.path.isdir('/usr/share/drat') else '/usr/local/share'
    parser = argparse.ArgumentParser(description='Text analysis tool', prog='drat', epilog=usage_info)
    parser.add_argument('infile', type=str, nargs='*', help='Name of file(s), or url(s) you want checked.')
    parser.add_argument('-w', dest='wordlist', type=argparse.FileType('r'),
            nargs='?', help='Name of additional wordlist(s) you want to use.')
    args = parser.parse_args()
    handler = ArgsHandler(args)
    handler.args_handler(base_dir)
