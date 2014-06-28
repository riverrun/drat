import unittest
import re
from drat.analysis import Checktext

class TestEmpty(unittest.TestCase):
    def test_no_sentences(self):
        data = ''
        sentences = len(re.findall('[\.!?]+', data)) or 1
        self.assertEqual(sentences, 1)

    def test_no_data(self):
        check = Checktext('None.txt', wlist=None, verb=False, web=False)
        with self.assertRaises(SystemExit) as exc:
            check.run_check('')
        self.assertEqual(exc.exception.code, 1)

    def test_raw_data(self):
        check = Checktext('None.txt', wlist=None, verb=False, web=False)
        result = check.run_check('small data')
        self.assertEqual(result, (0.0, 7.5))

class TestParrot(unittest.TestCase):
    def setUp(self):
        fname = 'parrot.txt'
        with open(fname, 'r') as f:
            self.data = f.read()
        self.sentences = len(re.findall('[\.!?]+', self.data)) or 1
        self.check = Checktext(fname, wlist=None, verb=False, web=True)

    def test_nums(self):
        self.assertEqual(self.sentences, 82)

    def test_raw_data(self):
        result = self.check.run_check(self.data)
        self.assertEqual(result, (7.5, 0.7))

class TestGrade1(unittest.TestCase):
    def setUp(self):
        fname = 'frog_toad.txt'
        with open(fname) as f:
            self.data = f.read()
        self.sentences = len(re.findall('[\.!?]+', self.data)) or 1
        self.check = Checktext(fname, wlist=None, verb=False, web=True)

    def test_sentences(self):
        self.assertEqual(self.sentences, 6)

    def test_raw_data(self):
        result = self.check.run_check(self.data)
        self.assertEqual(result, (5.7, -0.2))

class TestGrade5(unittest.TestCase):
    def setUp(self):
        fname = 'amphib.txt'
        with open(fname) as f:
            self.data = f.read()
        self.sentences = len(re.findall('[\.!?]+', self.data)) or 1
        self.check = Checktext(fname, wlist=None, verb=False, web=True)

    def test_sentences(self):
        self.assertEqual(self.sentences, 15)

    def test_raw_data(self):
        result = self.check.run_check(self.data)
        self.assertEqual(result, (7.3, 7.0))

class TestGrade13(unittest.TestCase):
    def setUp(self):
        fname = 'psych_today.txt'
        with open(fname) as f:
            self.data = f.read()
        self.sentences = len(re.findall('[\.!?]+', self.data)) or 1
        self.check = Checktext(fname, wlist=None, verb=False, web=True)

    def test_sentences(self):
        self.assertEqual(self.sentences, 6)

    def test_raw_data(self):
        result = self.check.run_check(self.data)
        self.assertEqual(result, (8.1, 14.6))

if __name__ == '__main__':
    unittest.main()
