from unittest import TestCase
from pyaddepar.reader import Reader, AddeparError


class TestReader(TestCase):

    # using the wrong connection details we can still instantiate the reader but throw an error as soon as we try to read data
    def test_init(self):
        r = Reader(id=1, key=2, secret=3)
        self.assertRaises(AddeparError, r.positions)
