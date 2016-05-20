
import itertools

import pandas as pd
from auth import aFirm, aKey, aSecret
from pyaddepar.graph.positions import Positions
from pyaddepar.graph.transactions import Transactions
from pyaddepar.reader import Reader
from sandbox.groups import Groups


if __name__ == '__main__':
    pd.set_option("display.width", 300)
    pd.set_option("display.max_rows", 300)
    pd.set_option('display.max_columns', None)

    # instantiate reader (e.g. wrapper of the addepar REST api)
    reader = Reader(id=aFirm, key=aKey, secret=aSecret)

    t = Transactions(reader.transactions().sortlevel(level="Owner ID"))
    print(t.transactions(id="804359", date=pd.Timestamp("2016-01-18")))