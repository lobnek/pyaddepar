from auth import aFirm, aKey, aSecret
import pandas as pd

if __name__ == '__main__':
    pd.set_option("display.width", 300)

    from pyaddepar.reader import Reader
    reader = Reader(id=aFirm, key=aKey, secret=aSecret)
    print(reader.groups)
    print(reader.positions())
    print(reader.transactions(start=pd.Timestamp("2016-01-01")))
    print(reader.entities())

