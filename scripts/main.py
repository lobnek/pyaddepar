#!/usr/bin/env python
import pandas as pd
from pyaddepar.preader import PReader

from pyaddepar.reader import Reader

if __name__ == '__main__':
    pd.set_option("display.width", 300)
    pd.set_option("display.max_rows", 300)
    pd.set_option('display.max_columns', None)

    # # instantiate reader (e.g. wrapper of the addepar REST api)
    reader = Reader()


    #assert False

    #print(reader.positions())
    #assert False

    #
    #e = reader.entities()
    #print(e)
    #print(e.keys())
    #print(e.ix["812752"])

    #p = reader.positions()
    #print(p.keys())

    t = reader.transactions()
    print(t.keys())
    print(t["Tag"])

    # print(e)
    # print(e.keys())
    # print(e.ix["804359"])


    r = PReader(id=aFirm, key=aKey, secret=aSecret)
    print(r)

    for group in r.groups:
        print(group)
        print(r.groups[group])

    #print(r.positions())
    #print(r.transactions)