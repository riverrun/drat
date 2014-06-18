import unittest
from collections import Counter
from drat.analysis import Checktext

class TestEmpty(unittest.TestCase):
    def test_no_sentences(self):
        data = b''
        sentences = data.count(b'.') + data.count(b'!') + data.count(b'?') or 1
        self.assertEqual(sentences, 1)

    def test_no_data(self):
        check = Checktext('None.txt', wlist=None, verb=False, web=False)
        with self.assertRaises(SystemExit) as exc:
            check.run_check(b'')
        self.assertEqual(exc.exception.code, 1)

    def test_raw_data(self):
        check = Checktext('None.txt', wlist=None, verb=False, web=False)
        result = check.run_check(b'small data')
        self.assertEqual(result, (2, Counter(), 0.1))

class TestParrot(unittest.TestCase):
    def setUp(self):
        fname = 'parrot.txt'
        with open(fname, 'rb') as f:
            self.data = f.read()
        self.sentences = self.data.count(b'.') + self.data.count(b'!') + self.data.count(b'?') or 1
        self.check = Checktext(fname, wlist=None, verb=False, web=True)
        self.count = Counter({'parrot': 9, 'ello': 4, 'nailed': 4, 'norwegian': 4, 'plumage': 3,
            'voom': 3, 'stunned': 3, 'fjords': 2, 'restin': 2, 'perch': 2, 'pinin': 2,
            'bleedin': 2, 'polly': 2, 'lad': 2, 'squire': 2, 'pining': 2, 'yelling': 1,
            'invisibile': 1, 'parrots': 1, 'choir': 1, 'nuzzled': 1, 'deceased': 1,
            'nit': 1, 'closin': 1, 'bereft': 1, 'peek': 1, 'kippin': 1, 'alf': 1,
            'volts': 1, 'mister': 1, 'wakin': 1, 'cuttle': 1, 'shuffled': 1, 'plummet': 1,
            'beak': 1, 'metabolic': 1, 'mortal': 1, 'daisies': 1, 'shagged': 1, 'istory': 1,
            'nononono': 1, 'slug': 1, 'ex': 1, 'id': 1, 'coil': 1, 'squawk': 1, 'boutique': 1,
            'twig': 1, 'init': 1, 'expired': 1, 'prolonged': 1, 'demised': 1, 'matey': 1,
            'ceased': 1, 'thumps': 1, 'stun': 1, 'nnnnot': 1})

    def test_sentences(self):
        self.assertEqual(self.sentences, 82)

    def test_raw_data(self):
        result = self.check.run_check(self.data)
        self.assertEqual(result, (270, self.count, 7.9))

class TestGrade1(unittest.TestCase):
    def setUp(self):
        fname = 'frog_toad.txt'
        with open(fname, 'rb') as f:
            self.data = f.read()
        self.sentences = self.data.count(b'.') + self.data.count(b'!') + self.data.count(b'?') or 1
        self.check = Checktext(fname, wlist=None, verb=False, web=True)
        self.count = Counter({'toad': 3})

    def test_sentences(self):
        self.assertEqual(self.sentences, 6)

    def test_raw_data(self):
        result = self.check.run_check(self.data)
        self.assertEqual(result, (39, self.count, 4.9))

class TestGrade5(unittest.TestCase):
    def setUp(self):
        fname = 'amphib.txt'
        with open(fname, 'rb') as f:
            self.data = f.read()
        self.sentences = self.data.count(b'.') + self.data.count(b'!') + self.data.count(b'?') or 1
        self.check = Checktext(fname, wlist=None, verb=False, web=True)
        self.count = Counter({'amphibian': 1, 'amphibians': 4, 'frog': 1, 'frogs': 2,
            'hatch': 2, 'jelly': 1, 'larvae': 1, 'salamanders': 1, 'tadpoles': 5, 'toad': 1, 'toads': 3})

    def test_sentences(self):
        self.assertEqual(self.sentences, 15)

    def test_raw_data(self):
        result = self.check.run_check(self.data)
        self.assertEqual(result, (86, self.count, 6.7))

class TestGrade13(unittest.TestCase):
    def setUp(self):
        fname = 'psych_today.txt'
        with open(fname, 'rb') as f:
            self.data = f.read()
        self.sentences = self.data.count(b'.') + self.data.count(b'!') + self.data.count(b'?') or 1
        self.check = Checktext(fname, wlist=None, verb=False, web=True)
        self.count = Counter({'sedate': 2, 'chlorpromazine': 1, 'synthesized': 1, 'opiates': 1,
            'surgical': 1, 'fogging': 1, 'bromides': 1, 'thorazine': 1, '’s': 1, 'ameliorate': 1,
            'manic': 1, 'antihistamine': 1, 'depressive': 1, 'intoxicated': 1, 'recipients': 1,
            'psychiatric': 1, 'schizophrenias': 1, 'psychoses': 1, 'barbiturates': 1})

    def test_sentences(self):
        self.assertEqual(self.sentences, 6)

    def test_raw_data(self):
        result = self.check.run_check(self.data)
        self.assertEqual(result, (79, self.count, 7.8))

class TestDCDict(unittest.TestCase):
    def setUp(self):
        self.check = Checktext('Example.txt', wlist=None, verb=False, web=True)
        self.count = Counter()

    def test_dale_chall_dict_1(self):
        self.check.fmt_output(270, self.count, 8.3)
        self.assertEqual(self.check.read_grade, ('Grades 11-12'))

    def test_dale_chall_dict_2(self):
        self.check.fmt_output(270, self.count, 4.9)
        self.assertEqual(self.check.read_grade, ('Grade 4 and below'))

    def test_dale_chall_dict_3(self):
        self.check.fmt_output(270, self.count, 5.6)
        self.assertEqual(self.check.read_grade, ('Grades 5-6'))

    def test_dale_chall_dict_4(self):
        self.check.fmt_output(270, self.count, 9.9)
        self.assertEqual(self.check.read_grade, ('Grades 13-15'))

    def test_dale_chall_dict_5(self):
        self.check.fmt_output(270, self.count, 10.0)
        self.assertEqual(self.check.read_grade, ('Grade 16 and above'))

if __name__ == '__main__':
    unittest.main()
