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
import textwrap
from . import analysis, parsers

def check_url(arg, wlist):
    try:
        response = requests.get(arg)
        html = response.text
        url_reader = parsers.HtmlParser()
        url_reader.feed(html)
        data = '\n'.join(url_reader.text)
    except:
        print('Sorry, can\'t open {}.'.format(arg))
        return
    check = analysis.Checktext(wlist)
    return check.run_check(data.lower())

def check_file(arg, wlist):
    exts = ('.docx', '.odt', '.ods', '.odp')
    if arg.endswith(exts):
        doc_reader = parsers.DocParser(arg)
        data = doc_reader.get_doctype()
    else:
        try:
            with open(arg) as f:
                data = f.read()
        except:
            print('Sorry, can\'t open {}.'.format(arg))
            return
    check = analysis.Checktext(wlist)
    return check.run_check(data.lower())

def fmt_output(name, verb, uncommon, uncom_len, uniq_len, dc_score, cli_score):
    dale_chall_grade = ((4.9, 'Grade 4 and below'), (5.9, 'Grades 5-6'), (6.9, 'Grades 7-8'),
            (7.9, 'Grades 9-10'), (8.9, 'Grades 11-12'), (9.9, 'Grades 13-15'))
    for key in dale_chall_grade:
        if dc_score <= key[0]:
            read_grade = key[1]
            break
    else:
        read_grade = 'Grade 16 and above'
    message = 'Report for {}.\n'.format(name)
    message += 'There are {:d} uncommon words in this text.\n'.format(uncom_len)
    message += 'This is out of a total of {:d} unique words.\n'.format(uniq_len)
    message += 'The Dale-Chall readability score is {:.1f} ({}).\n'.format(dc_score, read_grade)
    message += 'The Coleman-Liau Index is {:.1f}.\n'.format(cli_score)
    if verb:
        message += 'The following {:d} words are not in the list of common words:\n'.format(uncom_len)
        for item in uncommon.most_common():
            message += '{}: {}  '.format(item[0], item[1])
    return message

def start_check(arg, wordlist, verbose):
    if arg.startswith(('http', 'ftp')):
        result = check_url(arg, wordlist)
    else:
        result = check_file(arg, wordlist)
    return fmt_output(arg, verbose, *result)

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
        message = start_check(arg, wordlist, verbose)
        for line in message.splitlines():
            print(textwrap.fill(line, width=120))
