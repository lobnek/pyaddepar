from unittest import TestCase

import numpy as np
import pandas as pd

from pyaddepar.reader import Reader, AddeparError


class TestParser(TestCase):
    def test_b(self):
        x = Reader._Reader__parse([b"A,B", b"C,D"])
        self.assertEqual(list(x.keys()),["A","B"])
        self.assertEqual(list(x.index), [0])
        self.assertEqual(x["B"][0], "D")

    def test_empty(self):
        self.assertRaises(AddeparError, Reader._Reader__parse, [])

    def test_date_safe(self):
        self.assertEqual(Reader._Reader__date_safe("02/20/2016"), pd.Timestamp("20-02-2016").date())

    def test_date_safe_raises(self):
        # The month comes first!
        self.assertTrue(pd.isnull(Reader._Reader__date_safe("20/02/2016")))
        # empty strings also result in null/NaT
        self.assertTrue(pd.isnull(Reader._Reader__date_safe("")))

    def test_apply(self):
        A = np.array([["02/20/2016", "Peter Maffay", ""], ["", "", "-2"]])
        frame = Reader._Reader__apply(pd.DataFrame(data=A), dates=[0])

        self.assertEqual(frame[0][0], pd.Timestamp("20-02-2016").date())
        self.assertTrue(pd.isnull(frame[0][1]))

        self.assertEqual(frame[1][0], "Peter Maffay")
        self.assertEqual(frame[1][1], "")

        self.assertTrue(pd.isnull(frame[2][0]))
        self.assertEqual(frame[2][1], -2)
