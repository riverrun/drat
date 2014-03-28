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

import os
import json
import textwrap
from collections import Counter

base_dir = '/usr/local/share' if 'local' in os.path.split(__file__)[0].split('/') else '/usr/share'

class Checktext(object):
    def __init__(self, name, wlist, verb, web):
        self.name = name
        self.verb = verb
        self.web = web
        self.load_common(wlist)
        self.load_dale_chall()

    def load_common(self, wlist):
        """Create the dictionary of common words."""
        self.com_dict = os.path.join(base_dir, 'drat', 'EN_vocab.json')
        with open(self.com_dict) as words_file:
            data = json.load(words_file)
        self.common_words = Counter(data)
        if wlist:
            for new_words in wlist:
                new_dict = {word.strip() for word in new_words.splitlines()}
                self.common_words.update(new_dict)

    def load_dale_chall(self):
        """Create the dictionary of words, and grade dictionary, for the Dale-Chall readability test."""
        self.dale_chall_dict = os.path.join(base_dir, 'drat', 'dale_chall.json')
        with open(self.dale_chall_dict) as words_file:
            data = json.load(words_file)
        self.dale_chall_words = Counter(data)
        self.dale_chall_grade = {4.9: 'Grade 4 and below', 5.9: 'Grades 5-6', 6.9: 'Grades 7-8',
                7.9: 'Grades 9-10', 8.9: 'Grades 11-12', 9.9: 'Grades 13-15'}

    def load_file(self, words, sentences):
        """Count uncommon words and difficult words in file."""
        uniq_len = len(words)
        self.total = sum(words.values())
        common = words & self.common_words
        for word in common:
            words.pop(word)
        dchall_set = words & self.dale_chall_words
        diff_count = self.total - sum(dchall_set.values())
        dale_chall_score = round(self.dale_chall(diff_count, sentences), 1)
        self.fmt_output(uniq_len, words, dale_chall_score)

    def dale_chall(self, diff_count, sentences):
        """Calculate Dale-Chall readability score."""
        pdw = diff_count / self.total * 100
        asl = self.total / sentences
        raw = 0.1579 * (pdw) + 0.0496 * asl
        if pdw > 5:
            return raw + 3.6365
        return raw

    def fmt_output(self, uniq_len, uncommon, dale_chall_score):
        uncom_len = len(uncommon)
        for key in self.dale_chall_grade:
            if dale_chall_score < key:
                self.read_grade = self.dale_chall_grade[key]
                break
        else:
            self.read_grade = 'Grade 16 and above'
        self.message = 'Report for {}.\n'.format(self.name)
        self.message += 'There are {:d} uncommon words in this text.\n'.format(uncom_len)
        self.message += 'This is out of a total of {:d} unique words.\n'.format(uniq_len)
        self.message += 'The Dale-Chall readability score is {:.1f} ({}).\n'.format(dale_chall_score, self.read_grade)
        if self.verb:
            self.message += 'The following {:d} words are not in the list of common words:\n'.format(uncom_len)
            self.message += textwrap.fill('   '.join(list(uncommon)), width=80)
        if not self.web:
            print(self.message)
