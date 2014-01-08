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
import zipfile
import xml.etree.ElementTree as ET
import urllib.request
from html.parser import HTMLParser
from . import analysis

base_url = '/usr/share' if os.path.isdir('/usr/share/drat') else '/usr/local/share'

usage_info = """The 'infile' will be compared with a list of common English words, and a
report of the results will be saved in the current working directory."""

class HtmlParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.get_data = False

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.get_data = True

    def handle_endtag(self, tag):
        if tag == 'p':
            self.get_data = False

    def handle_data(self, data):
        if self.get_data:
            print(data)

class DocParser(object):
    def parse_doc(self, infile, docid):
        zfile = zipfile.ZipFile(infile)
        body = ET.fromstring(zfile.read(docid))
        text = '\n'.join([et.text.strip() for et in body.iter() if et.text])
        return text

def main():
    parser = argparse.ArgumentParser(description='Text analysis tool', prog='drat', epilog=usage_info)
    parser.add_argument('infile', type=argparse.FileType('r'), help='Name of file, or url, you want checked')
    args = parser.parse_args()
    print(args.infile.name)
    print(dir(args.infile))
    if args.infile.name.startswith('http'):
        response = urllib.request.urlopen(args.infile)
        html = str(response.read())
        reader = HtmlParser()
        data = reader.feed(html)
    else:
        reader = DocParser()
        if args.infile.name.endswith('.docx'):
            data = reader.parse_doc(args.infile.name, 'word/document.xml')
        else:
            data = reader.parse_doc(args.infile.name, 'content.xml')
    check = analysis.Checktext(base_url)
    check.load_words()
    check.load_file(data.splitlines())
