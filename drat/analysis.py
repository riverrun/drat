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
import string
import textwrap

base_dir = '/usr/local/share' if 'local' in os.path.split(__file__)[0].split('/') else '/usr/share'

class Checktext(object):
    def __init__(self, name, wordlist, web):
        self.name = name
        self.web = web
        self.load_common(wordlist)
        self.load_dale_chall()

    def load_common(self, wordlist):
        """Create the dictionary of common words."""
        self.com_dict = os.path.join(base_dir, 'drat', 'EN_vocab.json')
        with open(self.com_dict) as words_file:
            data = json.load(words_file)
        self.common_words = set(data)
        if wordlist:
            for new_words in wordlist:
                new_dict = {word.strip() for word in new_words.splitlines()}
                self.common_words.update(new_dict)

    def load_dale_chall(self):
        """Create the dictionary of words, and grade dictionary, for the Dale-Chall readability test."""
        self.dale_chall_dict = os.path.join(base_dir, 'drat', 'dale_chall.json')
        with open(self.dale_chall_dict) as words_file:
            data = json.load(words_file)
        self.dale_chall_words = set(data)
        self.dale_chall_grade = {4.9: 'Grade 4 and below', 5.9: 'Grades 5-6', 6.9: 'Grades 7-8',
                7.9: 'Grades 9-10', 8.9: 'Grades 11-12', 9.9: 'Grades 13-15'}

    def load_file(self, infile, sentences):
        self.table = {ord(c): ' ' for c in string.punctuation}
        words = [word.lower() for line in infile for word in line.translate(self.table).split() if word.isalpha()]
        self.total = len(words)
        self.check_common(words, sentences)

    def check_common(self, words, sentences):
        """Count uncommon words and difficult words."""
        unique_words = set()
        add_unique = unique_words.add
        uncommon = set()
        add_un = uncommon.add
        difficult = 0
        for word in words:
            add_unique(word)
            if word not in self.common_words:
                add_un(word)
            if word not in self.dale_chall_words:
                difficult += 1
        dale_chall_score = round(self.dale_chall(difficult, sentences))
        uniq_len = len(unique_words)
        self.fmt_output(uniq_len, uncommon, dale_chall_score)

    def dale_chall(self, difficult, sentences):
        pdw = difficult / self.total * 100
        asl = self.total / sentences
        raw = 0.1579 * (pdw) + 0.0496 * asl
        if pdw > 5:
            return raw + 3.6365
        return raw

    def write_report(self, text):
        name = self.name.translate(self.table).split()[-2]
        ls = os.listdir()
        for count in range(1, 100):
            filename = '{}_{:03d}.txt'.format(name, count)
            if filename not in ls:
                break
        with open(filename, 'w') as outfile:
            outfile.write(text)
        return filename

    def fmt_output(self, uniq_len, uncommon, dale_chall_score):
        uncom_len = len(uncommon)
        for key in self.dale_chall_grade:
            if dale_chall_score < key:
                self.read_grade = self.dale_chall_grade[key]
                break
        else:
            self.read_grade = 'Grades 16 and above'
        self.text = 'Report for {}.\n'.format(self.name)
        self.text += 'The Dale-Chall readability score for this text is {:.1f} ({}).\n'.format(dale_chall_score, self.read_grade)
        self.text += 'There are a total of {:d} unique words in the text.\n'.format(uniq_len)
        self.text += 'The following {:d} words are not in the list of common words:\n'.format(uncom_len)
        self.text += textwrap.fill('   '.join(list(uncommon)), width=80)
        self.message = 'There are {:d} uncommon words.\n'.format(uncom_len)
        self.message += 'The Dale-Chall readability score for this text is {:.1f} ({}).\n'.format(dale_chall_score, self.read_grade)
        if not self.web:
            report = self.write_report(self.text)
            self.message += 'For further details, read the {} file.'.format(report)
            print(self.message)
