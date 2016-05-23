import pandas as pd
from auth import aFirm, aKey, aSecret
from pyaddepar.preader import PReader

if __name__ == '__main__':
    pd.set_option("display.width", 300)
    pd.set_option("display.max_rows", 300)
    pd.set_option('display.max_columns', None)

    # instantiate reader (e.g. wrapper of the addepar REST api)
    reader = PReader(id=aFirm, key=aKey, secret=aSecret)

    # here we list transactions by 804361 and subsequent owners
    print(reader.transactions.left(["804361"]))

