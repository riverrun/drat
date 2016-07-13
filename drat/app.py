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
import click
import multiprocessing as MP
import requests
from functools import partial
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
        data = parsers.doc_reader(arg)
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
    message = [click.style('Report for {}\n\n'.format(name), bold=True, underline=True),
            'There are {:d} uncommon words in this text.\n'.format(uncom_len),
            'This is out of a total of {:d} unique words.\n'.format(uniq_len),
            'The Dale-Chall readability score is {:.1f} ({}).\n'.format(dc_score, read_grade),
            'The Coleman-Liau Index is {:.1f}.\n'.format(cli_score)]
    if verb:
        message.append('\nThese uncommon words are in the text:\n')
        count = 50 if verb == 1 else None
        message += ['{}: {}, '.format(item[0], item[1]) for item in uncommon.most_common(count)]
    return ''.join(message).rstrip(', ') + '\n'

def start_check(arg, wordlist, verbose):
    if arg.startswith(('http', 'ftp')):
        result = check_url(arg, wordlist)
    else:
        result = check_file(arg, wordlist)
    if result:
        return fmt_output(arg, verbose, *result)
    return 'There was an error checking {}.\n'.format(arg)

def raw_check(data):
    if not data:
        return 'No text to check.'
    check = analysis.Checktext(None)
    result = check.run_check(data.lower())
    return fmt_output('this text', True, *result)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('filenames', required=sys.stdin.isatty(), nargs=-1)
@click.option('--wordlist', '-w', type=click.Path(True), multiple=True,
        help='Name of wordlist file(s) to be used as an additional filter.')
@click.option('--verbose', '-v', count=True, help='List uncommon words.')
def cli(filenames, wordlist, verbose):
    """FILENAMES is the file, or url, you want analyzed.\n
    Multiple files, or urls, can be checked, and if possible, they will
    be checked in parallel.\n
    You can also provide a list of url links (with each link on a separate line)
    written in a text file. Each link in the file will then be checked.\n
    After the analysis, a report will be printed out. This report will print out
    the number of unique words in the text, the number of uncommon words (those
    words not in the General Service List), the Dale-Chall Readability Score
    (and the equivalent grade level), and the Coleman-Liau Readability Index.\n
    The verbose option, `-v`, will print out a list of the uncommon
    words that occurred the most times (the top 50). `-vv` will print out
    all of the uncommon words."""
    if not filenames:
        with sys.stdin as f:
            filenames = [arg.strip() for arg in f]
    run = partial(start_check, wordlist=wordlist, verbose=verbose)
    with MP.Pool(MP.cpu_count()) as p:
        reports = p.map(run, filenames)
    click.echo('\n'.join(reports))
