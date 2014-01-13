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
    def __init__(self, name, base_dir):
        self.name = name
        self.com_dict = os.path.join(base_dir, 'drat', 'EN_vocab')
        self.func_dict = os.path.join(base_dir, 'drat', 'EN_function')

    def load_common(self, wordlist):
        with open(self.com_dict) as words_file:
            data = words_file.read()
        self.common_words = {word for word in data.splitlines()}
        if wordlist:
            for new_words in wordlist:
                new_dict = {word.strip() for word in new_words}
                self.common_words.update(new_dict)

    def load_funcwords(self):
        with open(self.func_dict) as words_file:
            data = words_file.read()
        self.func_words = {word for word in data.splitlines()}

    def load_file(self, infile):
        table = {ord(c): ' ' for c in string.punctuation}
        words = [word.lower() for line in infile for word in line.translate(table).split() if word.isalpha()]
        self.total = len(words)
        self.check_common(words)

    def check_common(self, words):
        unique_words = set()
        add_unique = unique_words.add
        uncommon = set()
        add_un = uncommon.add
        lexi = 0
        for word in words:
            add_unique(word)
            if word not in self.func_words:
                lexi += 1
            if word not in self.common_words:
                add_un(word)
        uniq_len = len(unique_words)
        self.print_table(uniq_len, uncommon, lexi)

    def write_report(self, text):
        table = {ord(c): ' ' for c in 'htpw/.'}
        name = self.name.translate(table).split()[0]
        report = '{}_{:.2f}.txt'.format(name, time.time())
        with open(report, 'w') as outfile:
            outfile.write(text)
        return report

    def print_table(self, uniq_len, uncommon, lexi):
        uncom_len = len(uncommon)
        lex_density = lexi / self.total * 100
        text = 'Report for {}.\n'.format(self.name)
        text += 'The lexical density of this text is {:.2f}.\n'.format(lex_density)
        text += 'There are a total of {:d} unique words in the text.\n'.format(uniq_len)
        text += 'The following {:d} words are not in the list of common words:\n'.format(uncom_len)
        text += textwrap.fill('   '.join(list(uncommon)), width=80)
        report = self.write_report(text)
        print('There are {:d} uncommon words, and the lexical density is {:.2f}.'.format(uncom_len, lex_density))
        print('For further details, read the {} file.'.format(report))
