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

from __future__ import division
import sys
import os
import re
from collections import Counter

class Checktext(object):
    def __init__(self, wlist):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.load_common(wlist)
        self.load_dale_chall()

    def load_common(self, wlist):
        """Create the dictionary of common words."""
        self.com_dict = os.path.join(self.base_dir, 'dicts', 'EN_vocab.txt')
        with open(self.com_dict) as words_file:
            data = words_file.read()
        self.common_words = set(data.splitlines())
        if wlist:
            new_words = ''
            for wl in wlist:
                with open(wl) as f:
                    new_words += f.read()
            if new_words:
                new_dict = set(data.splitlines())
                self.common_words.update(new_dict)

    def load_dale_chall(self):
        """Create the dictionary of words, and grade dictionary, for the Dale-Chall readability test."""
        self.dale_chall_dict = os.path.join(self.base_dir, 'dicts', 'dale_chall.txt')
        with open(self.dale_chall_dict) as words_file:
            data = words_file.read()
        self.dale_chall_words = set(data.splitlines())

    def pre_check(self, data):
        """Count chars, words and sentences in the text."""
        sentences = len(re.findall('[\.!?]+\W+', data)) or 1
        chars = len(data) - len(re.findall('[^a-zA-Z0-9]', data))
        num_words = len(re.findall('\s+', data))
        data = re.split('[^a-zA-Z]+', data)
        return data, sentences, chars, num_words

    def run_check(self, data):
        """Check for uncommon words and difficult words in file."""
        if not data:
            sys.exit(1)
        data, sentences, chars, num_words = self.pre_check(data)
        w_dict = Counter(data)
        uniq_len, uncommon, uncom_len = self.gsl(w_dict)
        non_dchall_set = Counter({word: count for word, count in w_dict.items()
            if word and word not in self.dale_chall_words})
        diff_count = sum(non_dchall_set.values())
        dc_score = round(self.dale_chall(diff_count, num_words, sentences), 1)
        cli_score = round(self.coleman_liau(chars, num_words, sentences), 1)
        return uncommon, uncom_len, uniq_len, dc_score, cli_score

    def gsl(self, w_dict):
        uniq_len = len(w_dict)
        uncommon = Counter({word: count for word, count in w_dict.items()
            if word and word not in self.common_words})
        uncom_len = len(uncommon)
        return uniq_len, uncommon, uncom_len

    def dale_chall(self, diff_count, words, sentences):
        """Calculate Dale-Chall readability score."""
        pdw = diff_count / words * 100
        asl = words / sentences
        raw = 0.1579 * (pdw) + 0.0496 * asl
        if pdw > 5:
            return raw + 3.6365
        return raw

    def coleman_liau(self, chars, words, sentences):
        return 0.0588 * (chars / words * 100) - 0.296 * (sentences / words * 100) - 15.8
