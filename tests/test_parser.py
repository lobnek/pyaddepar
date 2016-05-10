from unittest import TestCase

import numpy as np
import pandas as pd

from pyaddepar.reader import AddeparError
from pyaddepar.parser import parse, request2frame


class TestParser(TestCase):
    def test_b(self):
        x = request2frame([b"A,B", b"C,D"])
        self.assertEqual(list(x.keys()),["A","B"])
        self.assertEqual(list(x.index), [0])
        self.assertEqual(x["B"][0], "D")

    def test_empty(self):
        self.assertRaises(AddeparError, request2frame, [])

    def test_apply(self):
        A = np.array([["02/20/2016", "Peter Maffay", ""], ["", "", "-2"]])
        frame = parse(pd.DataFrame(data=A), dates=[0], numbers=[2])

        self.assertEqual(frame[0][0], pd.Timestamp("20-02-2016").date())
        self.assertEqual(frame[1][0], "Peter Maffay")
        self.assertEqual(frame[1][1], "")
        self.assertEqual(frame[2][1], -2)
