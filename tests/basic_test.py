import unittest
from collections import Counter
from drat.analysis import Checktext

class TestDrat(unittest.TestCase):
    def setUp(self):
        fname = 'parrot.txt'
        with open(fname, 'rb') as f:
            data = f.read()
        self.sentences = data.count(b'.') + data.count(b'!') + data.count(b'?') or 1
        self.check = Checktext(fname, wlist=None, verb=False, web=False)
        self.result = self.check.run_check(data)

    def test_no_sentences(self):
        data = b''
        sentences = data.count(b'.') + data.count(b'!') + data.count(b'?') or 1
        self.assertEqual(sentences, 1)

    def test_sentences(self):
        self.assertEqual(self.sentences, 82)

    def test_raw_data(self):
        count = Counter({'parrot': 9, 'ello': 4, 'nailed': 4, 'norwegian': 4, 'plumage': 3,
            'voom': 3, 'stunned': 3, 'fjords': 2, 'restin': 2, 'perch': 2, 'pinin': 2,
            'bleedin': 2, 'polly': 2, 'lad': 2, 'squire': 2, 'pining': 2, 'yelling': 1,
            'invisibile': 1, 'parrots': 1, 'choir': 1, 'nuzzled': 1, 'deceased': 1,
            'nit': 1, 'closin': 1, 'bereft': 1, 'peek': 1, 'kippin': 1, 'alf': 1,
            'volts': 1, 'mister': 1, 'wakin': 1, 'cuttle': 1, 'shuffled': 1, 'plummet': 1,
            'beak': 1, 'metabolic': 1, 'mortal': 1, 'daisies': 1, 'shagged': 1, 'istory': 1,
            'nononono': 1, 'slug': 1, 'ex': 1, 'id': 1, 'coil': 1, 'squawk': 1, 'boutique': 1,
            'twig': 1, 'init': 1, 'expired': 1, 'prolonged': 1, 'demised': 1, 'matey': 1,
            'ceased': 1, 'thumps': 1, 'stun': 1, 'nnnnot': 1})
        self.assertEqual(self.result, (270, count, 8.3))

if __name__ == '__main__':
    unittest.main()
