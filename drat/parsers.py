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

import zipfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

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
            return data

class DocParser(object):
    def __init__(self, infile):
        self.infile = infile

    def get_doctype(self):
        if self.infile.endswith('.docx'):
            return self.parse_doc('word/document.xml')
        else:
            return self.parse_doc('content.xml')

    def parse_doc(self, docid):
        zfile = zipfile.ZipFile(self.infile)
        body = ET.fromstring(zfile.read(docid))
        text = '\n'.join([et.text.strip() for et in body.iter() if et.text])
        return text
