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
        self.sentences = 0
        self.args = args
        if not args.infile:
            with sys.stdin as f:
                data = f.read()
            self.args.infile = [arg for arg in data.splitlines()]

    def args_handler(self):
        for arg in self.args.infile:
            if arg.startswith('http'):
                self.check_url(arg)
            else:
                self.check_file(arg)

    def check_url(self, arg):
        response = requests.get(arg)
        html = response.text
        url_reader = parsers.HtmlParser()
        url_reader.feed(html)
        data = url_reader.text
        self.sentences = url_reader.sentences
        self.run_check(data, arg, self.args.wordlist)

    def check_file(self, arg):
        exts = ('.docx', '.odt', '.ods', '.odp')
        if arg.endswith(exts):
            doc_reader = parsers.DocParser(arg)
            data = doc_reader.get_doctype()
        else:
            with open(arg) as f:
                data = f.read()
        self.sentences += data.count('.') + data.count('!') + data.count('?')
        self.run_check(data.splitlines(), arg, self.args.wordlist)

    def run_check(self, data, name, wordlist):
        check = analysis.Checktext(name, wordlist, False)
        check.load_file(data, self.sentences)

def main():
    parser = argparse.ArgumentParser(description='Text analysis tool', prog='drat', epilog=usage_info)
    parser.add_argument('infile', type=str, nargs='*', help='Name of file(s), or url(s) you want checked.')
    parser.add_argument('-w', dest='wordlist', type=argparse.FileType('r'),
            nargs='?', help='Name of additional wordlist(s) you want to use.')
    args = parser.parse_args()
    handler = ArgsHandler(args)
    handler.args_handler()
