from auth import aFirm, aKey, aSecret
import pandas as pd

from pyaddepar.reader import Reader

if __name__ == '__main__':
    pd.set_option("display.width", 300)
    pd.set_option("display.max_rows", 300)
    pd.set_option('display.max_columns', None)

    # instantiate reader (e.g. wrapper of the addepar REST api)
    reader = Reader(id=aFirm, key=aKey, secret=aSecret)

    print(reader.groups)
    print(reader.positions())

    e = reader.entities()
    print(e)
    print(e.keys())
    print(e.ix["804359"])

