# Authors: David Whitlock <alovedalongthe@gmail.com>
# A simple text analysis tool
# Copyright (C) 2013-2016 David Whitlock
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

import sys
import zipfile
import xml.etree.ElementTree as ET
PY2 = sys.version_info[0] == 2
if PY2:
    from HTMLParser import HTMLParser
else:
    from html.parser import HTMLParser

class HtmlParser(HTMLParser):
    """Parse urls."""
    def __init__(self):
        HTMLParser.__init__(self)
        self.rem = '[]\r\n\t 0123456789'
        self.body = False
        self.get_data = False
        self.noscript = True
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.body = True
        if tag == 'script':
            self.noscript = False
        if tag == 'p':
            self.get_data = True

    def handle_endtag(self, tag):
        if tag == 'body':
            self.body = False
        if tag == 'script':
            self.noscript = True
        if tag == 'p':
            self.get_data = False

    def handle_data(self, data):
        if self.body and self.get_data and self.noscript and data.strip(self.rem):
            self.text.append(data)

def doc_reader(infile):
    """Parse docx and odf files."""
    if infile.endswith('.docx'):
        docid = 'word/document.xml'
    else:
        docid = 'content.xml'
    try:
        zfile = zipfile.ZipFile(infile)
    except:
        print('Sorry, can\'t open {}.'.format(infile))
        return
    body = ET.fromstring(zfile.read(docid))
    text = '\n'.join([et.text.strip() for et in body.iter() if et.text])
    return text
