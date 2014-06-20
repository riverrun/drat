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

import zipfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

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
        try:
            zfile = zipfile.ZipFile(self.infile)
        except:
            print('Sorry, can\'t open {}.'.format(self.infile))
            return
        body = ET.fromstring(zfile.read(docid))
        text = '\n'.join([et.text.strip() for et in body.iter() if et.text])
        return text.encode('utf-8')
