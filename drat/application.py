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

import sys
import click
import requests
from . import analysis, parsers

def check_url(arg, wlist, verb):
    try:
        response = requests.get(arg)
        html = response.text
        url_reader = parsers.HtmlParser()
        url_reader.feed(html)
        data = ''.join(url_reader.text)
    except:
        print('Sorry, can\'t open {}. Are you sure it exists?'.format(arg))
        return
    check = analysis.Checktext(arg, wlist, verb, False)
    check.run_check(data.encode('utf-8'))

def check_file(arg, wlist, verb):
    exts = ('.docx', '.odt', '.ods', '.odp')
    if arg.endswith(exts):
        doc_reader = parsers.DocParser(arg)
        data = doc_reader.get_doctype()
    else:
        try:
            with open(arg, 'rb') as f:
                data = f.read()
        except:
            print('Sorry, can\'t open {}. Are you sure it exists?'.format(arg))
            return
    check = analysis.Checktext(arg, wlist, verb, False)
    check.run_check(data)

@click.command()
@click.argument('filename', required=sys.stdin.isatty(), nargs=-1)
@click.option('--wordlist', '-w', type=click.Path(True), multiple=True,
        help='Name of wordlist file(s) to be used as an additional filter.')
@click.option('--verbose', '-v', count=True, help='Provide more detailed information.')
def cli(filename, wordlist, verbose):
    """FILENAME is the file, or url, you have chosen. This will be compared with
    lists of common English words, and a report of the results will be saved in
    the current working directory. It is possible to check multiple files.\n
    You can also provide a list of url links (with each link on a separate line)
    written in a text file. Each link in the file will then be checked."""
    if not filename:
        with sys.stdin as f:
            filename = [arg.strip() for arg in f]
    for arg in filename:
        if arg.startswith('http'):
            check_url(arg, wordlist, verbose)
        else:
            check_file(arg, wordlist, verbose)
