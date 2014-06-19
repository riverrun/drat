import unittest
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
        self.assertEqual(result, (0.1, -7.1))

class TestParrot(unittest.TestCase):
    def setUp(self):
        fname = 'parrot.txt'
        with open(fname, 'rb') as f:
            self.data = f.read()
        self.sentences = self.data.count(b'.') + self.data.count(b'!') + self.data.count(b'?') or 1
        self.check = Checktext(fname, wlist=None, verb=False, web=True)

    def test_sentences(self):
        self.assertEqual(self.sentences, 82)

    def test_raw_data(self):
        result = self.check.run_check(self.data)
        self.assertEqual(result, (7.8, 3.7))

class TestGrade1(unittest.TestCase):
    def setUp(self):
        fname = 'frog_toad.txt'
        with open(fname, 'rb') as f:
            self.data = f.read()
        self.sentences = self.data.count(b'.') + self.data.count(b'!') + self.data.count(b'?') or 1
        self.check = Checktext(fname, wlist=None, verb=False, web=True)

    def test_sentences(self):
        self.assertEqual(self.sentences, 6)

    def test_raw_data(self):
        result = self.check.run_check(self.data)
        self.assertEqual(result, (4.9, 2.6))

class TestGrade5(unittest.TestCase):
    def setUp(self):
        fname = 'amphib.txt'
        with open(fname, 'rb') as f:
            self.data = f.read()
        self.sentences = self.data.count(b'.') + self.data.count(b'!') + self.data.count(b'?') or 1
        self.check = Checktext(fname, wlist=None, verb=False, web=True)

    def test_sentences(self):
        self.assertEqual(self.sentences, 15)

    def test_raw_data(self):
        result = self.check.run_check(self.data)
        self.assertEqual(result, (6.7, 8.4))

class TestGrade13(unittest.TestCase):
    def setUp(self):
        fname = 'psych_today.txt'
        with open(fname, 'rb') as f:
            self.data = f.read()
        self.sentences = self.data.count(b'.') + self.data.count(b'!') + self.data.count(b'?') or 1
        self.check = Checktext(fname, wlist=None, verb=False, web=True)

    def test_sentences(self):
        self.assertEqual(self.sentences, 6)

    def test_raw_data(self):
        result = self.check.run_check(self.data)
        self.assertEqual(result, (7.8, 15.9))

if __name__ == '__main__':
    unittest.main()
