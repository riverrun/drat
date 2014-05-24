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
import zipfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from . import analysis

usage_info = """The file, or url, you have chosen will be compared with a list of
common English words, and a report of the results will be saved in the current working directory.
You can also provide a list of url links (with each link on a separate line) written in a text file."""

class ArgsHandler(object):
    """Handle the command line arguments."""
    def __init__(self, args):
        self.args = args
        if not args.infile:
            with sys.stdin as f:
                self.args.infile = [arg.strip() for arg in f]

    def args_handler(self):
        for arg in self.args.infile:
            if arg.startswith('http'):
                self.check_url(arg)
            else:
                self.check_file(arg)

    def check_url(self, arg):
        response = requests.get(arg)
        html = response.text
        url_reader = HtmlParser()
        url_reader.feed(html)
        data = ''.join(url_reader.text)
        check = analysis.Checktext(arg, self.args.wlist, self.args.verb, False)
        check.run_check(data.encode('utf-8'))

    def check_file(self, arg):
        exts = ('.docx', '.odt', '.ods', '.odp')
        if arg.endswith(exts):
            doc_reader = DocParser(arg)
            data = doc_reader.get_doctype()
        else:
            with open(arg, 'rb') as f:
                data = f.read()
        check = analysis.Checktext(arg, self.args.wlist, self.args.verb, False)
        check.run_check(data)

class HtmlParser(HTMLParser):
    """Parse urls."""
    def __init__(self):
        HTMLParser.__init__(self)
        self.body = False
        self.get_data = True
        self.text = []
        self.sentences = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.body = True
        if tag == 'p':
            self.get_data = True
        if tag == 'script' or tag == 'a':
            self.get_data = False

    def handle_endtag(self, tag):
        if tag == 'body':
            self.body = False
        if tag == 'p':
            self.get_data = False
        if tag == 'script' or tag == 'a':
            self.get_data = True

    def handle_data(self, data):
        if self.body and self.get_data:
            self.text.append(data)

class DocParser(object):
    """Parse docx and odf files."""
    def __init__(self, infile):
        self.infile = infile

    def get_doctype(self):
        if self.infile.endswith('.docx'):
            docid = 'word/document.xml'
        else:
            docid = 'content.xml'
        zfile = zipfile.ZipFile(self.infile)
        body = ET.fromstring(zfile.read(docid))
        text = '\n'.join([et.text.strip() for et in body.iter() if et.text])
        return text.encode('utf-8')

def main():
    parser = argparse.ArgumentParser(description='Text analysis tool', prog='drat', epilog=usage_info)
    parser.add_argument('infile', type=str, nargs='*', help='Name of file(s), or url(s) you want checked.')
    parser.add_argument('-v', '--verbose', dest='verb', action='store_true', help='Print more detailed information.')
    parser.add_argument('-w', '--wordlist', dest='wlist', type=str,
            nargs='?', help='Name of additional wordlist(s) you want to use.')
    args = parser.parse_args()
    handler = ArgsHandler(args)
    handler.args_handler()
