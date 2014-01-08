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
import string
import textwrap
import time

class Checktext(object):
    def __init__(self, base_url):
        self.com_dict = os.path.join(base_url, 'drat', 'EN_vocab')
        self.func_dict = os.path.join(base_url, 'drat', 'EN_function')

    def load_words(self):
        with open(self.com_dict) as words_file:
            data = words_file.read()
        self.common_words = {word for word in data.splitlines()}

    def load_file(self, infile):
        table = {ord(c): ' ' for c in string.punctuation}
        words = [word.lower() for line in infile for word in line.translate(table).split() if word.isalpha()]
        self.check_words(words)

    def check_words(self, words):
        unique_words = set()
        add_unique = unique_words.add
        uncommon = set()
        add_un = uncommon.add
        for word in words:
            add_unique(word)
            if word not in self.common_words:
                add_un(word)
        uniq_len = len(unique_words)
        self.print_table(uniq_len, uncommon)

    def print_table(self, uniq_len, uncommon):
        uncom_len = len(uncommon)
        text = 'There are a total of {:d} unique words in the text.\n'.format(uniq_len)
        text += 'The following {:d} words are not in the list of common words:\n'.format(uncom_len)
        text += textwrap.fill('   '.join(list(uncommon)), width=80)
        report = '{}_report.txt'.format(time.strftime('%d%m_%H%M'))
        with open(report, 'w') as outfile:
            outfile.write(text)
        print('There are {:d} uncommon words in this text.'.format(uncom_len))
        print('For further details, read the {} file.'.format(report))
